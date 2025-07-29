# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""Utility Functions for Workflow Operations.

This module provides essential utility functions used throughout the workflow
system for ID generation, datetime handling, string processing, template
operations, and other common tasks.

Functions:
    gen_id: Generate unique identifiers for workflow components
    make_exec: Create executable strings for shell commands
    filter_func: Filter functions based on criteria
    dump_all: Serialize data to various formats
    delay: Create delays in execution
    to_train: Convert strings to train-case format
    get_dt_now: Get current datetime with timezone
    get_d_now: Get current date
    cross_product: Generate cross product of matrix values
    replace_sec: Replace template variables in strings

Example:
    ```python
    from ddeutil.workflow.utils import gen_id, get_dt_now

    # Generate unique ID
    run_id = gen_id("workflow")

    # Get current datetime
    now = get_dt_now()
    ```
"""
from __future__ import annotations

import stat
import time
from collections.abc import Iterator
from datetime import date, datetime, timedelta
from hashlib import md5
from inspect import isclass, isfunction
from itertools import product
from pathlib import Path
from random import randrange
from typing import Any, Final, Optional, TypeVar, Union, overload
from zoneinfo import ZoneInfo

from ddeutil.core import hash_str
from pydantic import BaseModel

from .__types import DictData, Matrix

T = TypeVar("T")
UTC: Final[ZoneInfo] = ZoneInfo("UTC")
MARK_NEWLINE: Final[str] = "||"

# Cache for random delay values to avoid repeated randrange calls
_CACHED_DELAYS = [randrange(0, 99, step=10) / 100 for _ in range(100)]
_DELAY_INDEX = 0


def to_train(camel: str) -> str:
    """Convert camel case string to train case.

    Args:
        camel: A camel case string that want to convert.

    Returns:
        str: The converted train-case string.
    """
    return "".join("-" + i if i.isupper() else i for i in camel).lstrip("-")


def prepare_newline(msg: str) -> str:
    """Prepare message that has multiple newline char.

    Args:
        msg: A message that want to prepare.

    Returns:
        str: The prepared message with formatted newlines.
    """
    # NOTE: Remove ending with "\n" and replace "\n" with the "||" value.
    msg: str = msg.strip("\n").replace("\n", MARK_NEWLINE)
    if MARK_NEWLINE not in msg:
        return msg

    msg_lines: list[str] = msg.split(MARK_NEWLINE)
    msg_last: str = msg_lines[-1]
    msg_body: str = (
        "\n" + "\n".join(f" ... |  \t{s}" for s in msg_lines[1:-1])
        if len(msg_lines) > 2
        else ""
    )
    return msg_lines[0] + msg_body + f"\n ... ╰─ \t{msg_last}"


def replace_sec(dt: datetime) -> datetime:
    """Replace second and microsecond values to 0.

    Args:
        dt: A datetime object that want to replace.

    Returns:
        datetime: The datetime with seconds and microseconds set to 0.
    """
    return dt.replace(second=0, microsecond=0)


def clear_tz(dt: datetime) -> datetime:
    """Replace timezone info on an input datetime object to None."""
    return dt.replace(tzinfo=None)


def get_dt_now(tz: Optional[ZoneInfo] = None, offset: float = 0.0) -> datetime:
    """Return the current datetime object.

    :param tz: A ZoneInfo object for replace timezone of return datetime object.
    :param offset: An offset second value.

    :rtype: datetime
    :return: The current datetime object that use an input timezone or UTC.
    """
    return datetime.now(tz=tz) - timedelta(seconds=offset)


def get_dt_ntz_now() -> datetime:  # pragma: no cov
    """Get current datetime with no timezone.

    Returns the current datetime object using the None timezone.

    Returns:
        datetime: Current datetime with no timezone
    """
    return get_dt_now(tz=None)


def get_d_now(
    tz: Optional[ZoneInfo] = None, offset: float = 0.0
) -> date:  # pragma: no cov
    """Return the current date object.

    :param tz: A ZoneInfo object for replace timezone of return date object.
    :param offset: An offset second value.

    :rtype: date
    :return: The current date object that use an input timezone or UTC.
    """
    return (datetime.now(tz=tz) - timedelta(seconds=offset)).date()


def get_diff_sec(dt: datetime, offset: float = 0.0) -> int:
    """Return second value that come from diff of an input datetime and the
    current datetime with specific timezone.

    :param dt: (datetime) A datetime object that want to get different second value.
    :param offset: (float) An offset second value.

    :rtype: int
    """
    return round(
        (
            dt - datetime.now(tz=dt.tzinfo) - timedelta(seconds=offset)
        ).total_seconds()
    )


def reach_next_minute(dt: datetime, offset: float = 0.0) -> bool:
    """Check this datetime object is not in range of minute level on the current
    datetime.

    :param dt: (datetime) A datetime object that want to check.
    :param offset: (float) An offset second value.
    """
    diff: float = (
        replace_sec(clear_tz(dt)) - replace_sec(get_dt_now(offset=offset))
    ).total_seconds()
    if diff >= 60:
        return True
    elif diff >= 0:
        return False
    raise ValueError(
        "Check reach the next minute function should check a datetime that not "
        "less than the current date"
    )


def wait_until_next_minute(
    dt: datetime, second: float = 0
) -> None:  # pragma: no cov
    """Wait with sleep to the next minute with an offset second value."""
    future: datetime = replace_sec(dt) + timedelta(minutes=1)
    time.sleep((future - dt).total_seconds() + second)


def delay(second: float = 0) -> None:  # pragma: no cov
    """Delay time that use time.sleep with random second value between
    0.00 - 0.99 seconds.

    :param second: (float) A second number that want to adds-on random value.
    """
    global _DELAY_INDEX
    cached_random = _CACHED_DELAYS[_DELAY_INDEX % len(_CACHED_DELAYS)]
    _DELAY_INDEX = (_DELAY_INDEX + 1) % len(_CACHED_DELAYS)
    time.sleep(second + cached_random)


def gen_id(
    value: Any,
    *,
    sensitive: bool = True,
    unique: bool = False,
    simple_mode: Optional[bool] = None,
    extras: DictData | None = None,
) -> str:
    """Generate running ID for able to tracking. This generates process use
    ``md5`` algorithm function if ``WORKFLOW_CORE_WORKFLOW_ID_SIMPLE_MODE`` set
    to false. But it will cut this hashing value length to 10 it the setting
    value set to true.

    Simple Mode:

        ... 0000 00    00  00   00     00     000000       T    0000000000
        ... year month day hour minute second microsecond  sep  simple-id

    :param value: A value that want to add to prefix before hashing with md5.
    :param sensitive: (bool) A flag that enable to convert the value to lower
        case before hashing that value before generate ID.
    :param unique: (bool) A flag that add timestamp at microsecond level to
        value before hashing.
    :param simple_mode: (bool | None) A flag for generate ID by simple mode.
    :param extras: (DictData) An extra parameter that use for override config
        value.

    :rtype: str
    """
    from .conf import dynamic

    if not isinstance(value, str):
        value: str = str(value)

    dt: datetime = datetime.now(tz=dynamic("tz", extras=extras))
    if dynamic("generate_id_simple_mode", f=simple_mode, extras=extras):
        return (f"{dt:%Y%m%d%H%M%S%f}T" if unique else "") + hash_str(
            f"{(value if sensitive else value.lower())}", n=10
        )

    return md5(
        (
            (f"{dt}T" if unique else "")
            + f"{(value if sensitive else value.lower())}"
        ).encode()
    ).hexdigest()


def default_gen_id() -> str:
    """Return running ID which use for making default ID for the Result model if
    a run_id field initializes at the first time.

    :rtype: str
    """
    return gen_id("manual", unique=True)


def make_exec(path: Union[Path, str]) -> None:
    """Change mode of file to be executable file.

    :param path: (Path | str) A file path that want to make executable
        permission.
    """
    f: Path = Path(path) if isinstance(path, str) else path
    f.chmod(f.stat().st_mode | stat.S_IEXEC)


def filter_func(value: T) -> T:
    """Filter out an own created function of any value of mapping context by
    replacing it to its function name. If it is built-in function, it does not
    have any changing.

    :param value: A value context data that want to filter out function value.
    :type: The same type of input ``value``.
    """
    if isinstance(value, dict):
        return {k: filter_func(value[k]) for k in value}
    elif isinstance(value, (list, tuple, set)):
        return type(value)([filter_func(i) for i in value])

    if isfunction(value):
        # NOTE: If it wants to improve to get this function, it is able to save
        # to some global memory storage.
        #   ---
        #   >>> GLOBAL_DICT[value.__name__] = value
        #
        return value.__name__
    return value


def cross_product(matrix: Matrix) -> Iterator[DictData]:
    """Iterator of products value from matrix.

    :param matrix: (Matrix)

    :rtype: Iterator[DictData]
    """
    yield from (
        {_k: _v for e in mapped for _k, _v in e.items()}
        for mapped in product(
            *[[{k: v} for v in vs] for k, vs in matrix.items()]
        )
    )


def cut_id(run_id: str, *, num: int = 6) -> str:
    """Cutting running ID with length.

    Example:
        >>> cut_id(run_id='20240101081330000000T1354680202')
        '202401010813680202'

    :param run_id: (str) A running ID That want to cut.
    :param num: (int) A number of cutting length.

    :rtype: str
    """
    if "T" in run_id:
        dt, simple = run_id.split("T", maxsplit=1)
        return dt[:12] + simple[-num:]
    return run_id[:12] + run_id[-num:]


@overload
def dump_all(
    value: BaseModel, by_alias: bool = False
) -> DictData: ...  # pragma: no cov


@overload
def dump_all(value: T, by_alias: bool = False) -> T: ...  # pragma: no cov


def dump_all(
    value: Union[T, BaseModel],
    by_alias: bool = False,
) -> Union[T, DictData]:
    """Dump all nested BaseModel object to dict object.

    :param value: (T | BaseModel)
    :param by_alias: (bool)
    """
    if isinstance(value, dict):
        return {k: dump_all(value[k], by_alias=by_alias) for k in value}
    elif isinstance(value, (list, tuple, set)):
        return type(value)([dump_all(i, by_alias=by_alias) for i in value])
    elif isinstance(value, BaseModel):
        return value.model_dump(by_alias=by_alias)
    return value


def obj_name(obj: Optional[Union[str, object]] = None) -> Optional[str]:
    if not obj:
        obj_type: Optional[str] = None
    elif isinstance(obj, str):
        obj_type: str = obj
    elif isclass(obj):
        obj_type: str = obj.__name__
    else:
        obj_type: str = obj.__class__.__name__
    return obj_type
