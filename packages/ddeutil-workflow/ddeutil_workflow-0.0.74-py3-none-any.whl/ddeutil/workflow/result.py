# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""Result and Status Management Module.

This module provides the core result and status management functionality for
workflow execution tracking. It includes the Status enumeration for execution
states and the Result dataclass for context transfer between workflow components.

Classes:
    Status: Enumeration for execution status tracking
    Result: Dataclass for execution context and result management

Functions:
    validate_statuses: Determine final status from multiple status values
    get_status_from_error: Convert exception types to appropriate status
    get_dt_tznow: Get current datetime with timezone configuration
"""
from __future__ import annotations

from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from pydantic.functional_validators import model_validator
from typing_extensions import Self

from . import (
    JobCancelError,
    JobError,
    JobSkipError,
    StageCancelError,
    StageError,
    StageSkipError,
    WorkflowCancelError,
    WorkflowError,
)
from .__types import DictData
from .audits import Trace, get_trace
from .errors import ResultError
from .utils import default_gen_id, get_dt_ntz_now


class Status(str, Enum):
    """Execution status enumeration for workflow components.

    Status enum provides standardized status values for tracking the execution
    state of workflows, jobs, and stages. Each status includes an emoji
    representation for visual feedback.

    Attributes:
        SUCCESS: Successful execution completion
        FAILED: Execution failed with errors
        WAIT: Waiting for execution or dependencies
        SKIP: Execution was skipped due to conditions
        CANCEL: Execution was cancelled
    """

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    WAIT = "WAIT"
    SKIP = "SKIP"
    CANCEL = "CANCEL"

    @property
    def emoji(self) -> str:  # pragma: no cov
        """Get emoji representation of the status.

        Returns:
            str: Unicode emoji character representing the status
        """
        return {
            "SUCCESS": "✅",
            "FAILED": "❌",
            "WAIT": "🟡",
            "SKIP": "⏩",
            "CANCEL": "🚫",
        }[self.name]

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def is_result(self) -> bool:
        return self in ResultStatuses


SUCCESS = Status.SUCCESS
FAILED = Status.FAILED
WAIT = Status.WAIT
SKIP = Status.SKIP
CANCEL = Status.CANCEL

ResultStatuses: list[Status] = [SUCCESS, FAILED, CANCEL, SKIP]


def validate_statuses(statuses: list[Status]) -> Status:
    """Determine final status from multiple status values.

    Applies workflow logic to determine the overall status based on a collection
    of individual status values. Follows priority order: CANCEL > FAILED > WAIT >
    individual status consistency.

    Args:
        statuses: List of status values to evaluate

    Returns:
        Status: Final consolidated status based on workflow logic

    Example:
        ```python
        # Mixed statuses - FAILED takes priority
        result = validate_statuses([SUCCESS, FAILED, SUCCESS])
        # Returns: FAILED

        # All same status
        result = validate_statuses([SUCCESS, SUCCESS, SUCCESS])
        # Returns: SUCCESS
        ```
    """
    if any(s == CANCEL for s in statuses):
        return CANCEL
    elif any(s == FAILED for s in statuses):
        return FAILED
    elif any(s == WAIT for s in statuses):
        return WAIT
    for status in (SUCCESS, SKIP):
        if all(s == status for s in statuses):
            return status
    return FAILED if FAILED in statuses else SUCCESS


def get_status_from_error(
    error: Union[
        StageError,
        StageCancelError,
        StageSkipError,
        JobError,
        JobCancelError,
        JobSkipError,
        WorkflowError,
        WorkflowCancelError,
        Exception,
        BaseException,
    ]
) -> Status:
    """Get the Status from the error object.

    Returns:
        Status: The status from the specific exception class.
    """
    if isinstance(error, (StageSkipError, JobSkipError)):
        return SKIP
    elif isinstance(
        error, (StageCancelError, JobCancelError, WorkflowCancelError)
    ):
        return CANCEL
    return FAILED


def default_context() -> DictData:
    return {"status": WAIT}


@dataclass(
    config=ConfigDict(arbitrary_types_allowed=True, use_enum_values=True),
)
class Result:
    """Result Pydantic Model for passing and receiving data context from any
    module execution process like stage execution, job execution, or workflow
    execution.

        For comparison property, this result will use ``status``, ``context``,
    and ``_run_id`` fields to comparing with other result instance.

    Warning:
        I use dataclass object instead of Pydantic model object because context
    field that keep dict value change its ID when update new value to it.
    """

    status: Status = field(default=WAIT)
    context: DictData = field(default_factory=default_context)
    info: DictData = field(default_factory=dict)
    run_id: Optional[str] = field(default_factory=default_gen_id)
    parent_run_id: Optional[str] = field(default=None, compare=False)
    ts: datetime = field(default_factory=get_dt_ntz_now, compare=False)
    trace: Optional[Trace] = field(default=None, compare=False, repr=False)
    extras: DictData = field(default_factory=dict, compare=False, repr=False)

    @model_validator(mode="after")
    def __prepare_trace(self) -> Self:
        """Prepare trace field that want to pass after its initialize step.

        :rtype: Self
        """
        if self.trace is None:  # pragma: no cov
            self.trace: Trace = get_trace(
                self.run_id,
                parent_run_id=self.parent_run_id,
                extras=self.extras,
            )
        return self

    def set_parent_run_id(self, running_id: str) -> Self:
        """Set a parent running ID.

        :param running_id: (str) A running ID that want to update on this model.

        :rtype: Self
        """
        self.parent_run_id: str = running_id
        self.trace: Trace = get_trace(
            self.run_id, parent_run_id=running_id, extras=self.extras
        )
        return self

    def catch(
        self,
        status: Union[int, Status],
        context: DictData | None = None,
        **kwargs,
    ) -> Self:
        """Catch the status and context to this Result object. This method will
        use between a child execution return a result, and it wants to pass
        status and context to this object.

        :param status: A status enum object.
        :param context: A context data that will update to the current context.

        :rtype: Self
        """
        self.__dict__["context"].update(context or {})
        self.__dict__["status"] = (
            Status(status) if isinstance(status, int) else status
        )
        self.__dict__["context"]["status"] = self.status

        # NOTE: Update other context data.
        if kwargs:
            for k in kwargs:
                if k in self.__dict__["context"]:
                    self.__dict__["context"][k].update(kwargs[k])
                # NOTE: Exclude the `info` key for update information data.
                elif k == "info":
                    self.__dict__["info"].update(kwargs["info"])
                else:
                    raise ResultError(
                        f"The key {k!r} does not exists on context data."
                    )
        return self

    def make_info(self, data: DictData) -> Self:
        """Making information."""
        self.__dict__["info"].update(data)
        return self

    def alive_time(self) -> float:  # pragma: no cov
        """Return total seconds that this object use since it was created.

        :rtype: float
        """
        return (get_dt_ntz_now() - self.ts).total_seconds()


def catch(
    context: DictData,
    status: Union[int, Status],
    updated: DictData | None = None,
    **kwargs,
) -> DictData:
    """Catch updated context to the current context."""
    context.update(updated or {})
    context["status"] = Status(status) if isinstance(status, int) else status

    if not kwargs:
        return context

    # NOTE: Update other context data.
    for k in kwargs:
        if k in context:
            context[k].update(kwargs[k])
        # NOTE: Exclude the `info` key for update information data.
        elif k == "info":
            context["info"].update(kwargs["info"])
        else:
            raise ResultError(f"The key {k!r} does not exists on context data.")
    return context
