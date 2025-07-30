# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import calendar
import enum
import re
from datetime import date, datetime, timedelta, timezone
from typing import (
    Literal,
    Optional,
    Union,
)
from zoneinfo import ZoneInfo

try:
    from dateutil.parser import parse
    from dateutil.relativedelta import relativedelta
except ImportError:  # pragma: no cov
    relativedelta = None
    parse = None

from . import first

LOCAL_TZ: ZoneInfo = ZoneInfo("UTC")

DatetimeMode = Literal[
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second",
    "microsecond",
]
DATETIME_SET: tuple[str, ...] = (
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second",
    "microsecond",
)

FrequencyMode = Literal["1T", "1H", "1D", "1M", "1Y"]
FREQUENCY_SET: tuple[str, ...] = ("1T", "1H", "1D", "1M", "1Y")
_TIMEZONE_CACHE: dict[int, timezone] = {0: timezone.utc}
# Pre-compiled regex for better performance
_DATETIME_PATTERN: re.Pattern[str] = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})"  # YYYY-MM-DD
    r"(?:[T\s](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?)?"  # Optional time with microseconds
    r"(?:(Z)|([+-])(\d{2}):?(\d{2}))?$"  # Optional timezone
)


def _get_timezone(offset_minutes: int) -> timezone:  # pragma: no cov
    """Get timezone object from cache or create new one."""
    if offset_minutes not in _TIMEZONE_CACHE:
        _TIMEZONE_CACHE[offset_minutes] = timezone(
            timedelta(minutes=offset_minutes)
        )
    return _TIMEZONE_CACHE[offset_minutes]


def parse_dt_default(dt: Union[datetime, date, str]) -> datetime:
    """Parse datetime string using only Python built-in packages.

    Supports formats:
    - YYYY-MM-DD
    - YYYY-MM-DD HH:MM:SS[.ffffff]
    - YYYY-MM-DD HH:MM:SS[.ffffff]Z
    - YYYY-MM-DD HH:MM:SS[.ffffff]±HH:MM

    Args:
        dt: A datetime object or string to parse

    Returns:
        datetime: Parsed datetime object with appropriate timezone

    Raises:
        ValueError: If the input cannot be parsed
    """
    # Handle datetime objects directly
    if isinstance(dt, datetime):
        return dt

    # Handle date objects (convert to datetime at midnight)
    if isinstance(dt, date):
        return datetime(dt.year, dt.month, dt.day)

    # Handle string parsing
    if not isinstance(dt, str):
        raise ValueError("Input must be datetime, date, or string")

    match = _DATETIME_PATTERN.match(dt.strip())
    if not match:
        raise ValueError(f"Unable to parse datetime string: {dt}")

    (
        year,
        month,
        day,
        hour,
        minute,
        second,
        microsecond_str,
        utc_z,
        tz_sign,
        tz_hour,
        tz_minute,
    ) = match.groups()

    # Convert required components
    year, month, day = int(year), int(month), int(day)
    hour = int(hour) if hour else 0
    minute = int(minute) if minute else 0
    second = int(second) if second else 0

    # Handle microseconds efficiently
    microsecond = 0
    if microsecond_str:
        # Normalize to 6 digits and convert
        microsecond_str = microsecond_str.ljust(6, "0")[:6]
        microsecond = int(microsecond_str)

    # Handle timezone
    tz = None
    if utc_z:
        tz = timezone.utc
    elif tz_sign and tz_hour and tz_minute:
        offset_minutes = int(tz_hour) * 60 + int(tz_minute)
        if tz_sign == "-":
            offset_minutes = -offset_minutes
        tz = _get_timezone(offset_minutes)

    return datetime(year, month, day, hour, minute, second, microsecond, tz)


def parse_dt(dt: Union[datetime, str], **kwargs) -> datetime:
    """Parse datetime string using dateutil and return datetime object.

    :param dt: A datetime value that want to parse.
    """
    try:
        return parse_dt_default(dt)
    except ValueError:
        # NOTE: Fallback to dateutil for complex formats
        try:  # pragma: no cov
            from dateutil.parser import parse
            from dateutil.tz import tzoffset
        except ImportError as e:
            raise ValueError(
                f"Unable to parse '{dt}' with built-in parser. "
                "Install `dateutil` for complex datetime parsing: pip install "
                "`python-dateutil`."
            ) from e

        if isinstance(dt, str):
            dt = parse(dt, **kwargs)

        if isinstance(dt, date) and not isinstance(dt, datetime):
            return datetime(dt.year, dt.month, dt.day)

        if isinstance(dt, datetime):
            # Convert dateutil timezone to built-in timezone
            if dt.tzinfo and isinstance(dt.tzinfo, tzoffset):
                offset_seconds = int(dt.utcoffset().total_seconds())
                if offset_seconds == 0:
                    return dt.replace(tzinfo=timezone.utc)
                else:
                    offset_minutes = offset_seconds // 60
                    return dt.replace(tzinfo=_get_timezone(offset_minutes))
            return dt

        raise ValueError(f"Unable to parse datetime: {dt}") from None


def get_datetime_replace(
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> dict[str, tuple]:
    return {
        "year": (1990, 9999),
        "month": (1, 12),
        "day": (
            1,
            (calendar.monthrange(year, month)[1] if year and month else 31),
        ),
        "hour": (0, 23),
        "minute": (0, 59),
        "second": (0, 59),
        "microsecond": (0, 999999),
    }


class DatetimeDim(enum.IntEnum):
    """Datetime dimension enum object."""

    MICROSECOND = 0
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    MONTH = 5
    YEAR = 6

    @classmethod
    def get_dim(cls, value: str) -> int:
        """Get dimension value from a datetime mode.

        :rtype: int
        """
        if hasattr(cls, value.upper()):
            return getattr(cls, value.upper())
        raise ValueError(
            f"Datetime dimension does not contain dimension for {value!r}"
        )


def get_date(
    fmt: str,
    *,
    _tz: Optional[Union[str, ZoneInfo]] = None,
) -> Union[datetime, datetime.date, str]:
    """Return the current datetime with custom string format.

    Examples:
        >>> get_date(fmt='%Y-%m-%d')
        '2023-01-01'
    """
    if _tz is None:
        _tz: ZoneInfo = LOCAL_TZ
    elif isinstance(_tz, str):
        _tz: ZoneInfo = ZoneInfo(_tz)
    else:
        _tz: ZoneInfo = _tz

    _datetime: datetime = datetime.now(_tz)
    if fmt == "datetime":
        return _datetime
    elif fmt == "date":
        return _datetime.date()
    return _datetime.strftime(fmt)


def replace_date(
    dt: datetime,
    mode: DatetimeMode,
    reverse: bool = False,
) -> datetime:
    """Replace datetime matrix that less than an input mode to origin value.

    :param dt: A datetime value that want to replace.
    :param mode: A mode to repalce datetime.
    :param reverse: A reverse flag.

    Examples:
        >>> replace_date(datetime(2023, 1, 31, 13, 2, 47), mode='day')
        datetime.datetime(2023, 1, 31, 0, 0)
        >>> replace_date(datetime(2023, 3, 25, 13, 2, 47), mode='year')
        datetime.datetime(2023, 1, 1, 0, 0)
    """
    assert mode in (
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
    )
    replace_mapping: dict[str, tuple] = get_datetime_replace(dt.year, dt.month)
    return dt.replace(
        **{
            _.name.lower(): replace_mapping[_.name.lower()][int(reverse)]
            for _ in DatetimeDim
            if _ < DatetimeDim.get_dim(mode)
        }
    )


def next_date(
    dt: datetime,
    mode: DatetimeMode,
    *,
    reverse: bool = False,
    next_value: int = 1,
) -> datetime:
    """Return the next date with specific unit mode.

    Examples:
        >>> next_date(datetime(2023, 1, 31, 0, 0, 0), mode='day')
        datetime.datetime(2023, 2, 1, 0, 0)
        >>> next_date(datetime(2023, 1, 31, 0, 0, 0), mode='month')
        datetime.datetime(2023, 2, 28, 0, 0)
        >>> next_date(datetime(2023, 1, 31, 0, 0, 0), mode='hour')
        datetime.datetime(2023, 1, 31, 1, 0)
        >>> next_date(datetime(2023, 1, 31, 0, 0, 0), mode='year')
        datetime.datetime(2024, 1, 31, 0, 0)
    """
    if relativedelta is None:
        raise ImportError(
            "This function require relativedelta from the dateutil package, "
            "you should install with `pip install ddeutil[dateutil]`"
        )
    assert mode in (
        "year",
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
    )
    assert -1000 <= next_value <= 1000
    return dt + relativedelta(
        **{f"{mode}s": (-next_value if reverse else next_value)}
    )


def closest_quarter(dt: datetime) -> datetime:
    """Return closest quarter datetime of an input datetime.

    :param dt: A datetime value that want to convert.
    :rtype: datetime

    Examples:
        >>> closest_quarter(datetime(2024, 9, 25))
        datetime.datetime(2024, 9, 30, 0, 0)
        >>> closest_quarter(datetime(2024, 2, 13))
        datetime.datetime(2023, 12, 31, 0, 0)
    """
    # NOTE: candidate list, nicely enough none of these are in February, so
    #   the month lengths are fixed
    candidates: list[datetime] = [
        datetime(dt.year - 1, 12, 31, 0),
        datetime(dt.year, 3, 31, 0),
        datetime(dt.year, 6, 30, 0),
        datetime(dt.year, 9, 30, 0),
        datetime(dt.year, 12, 31, 0),
    ]
    # NOTE: take the minimum according to the absolute distance to the target
    #   date.
    return min(candidates, key=lambda d: abs(dt - d))


def last_dom(dt: datetime) -> datetime:
    """Get the latest day of month that relate with an input datetime value.
    :param dt:
    :rtype: datetime

    Examples:
        >>> last_dom(datetime(2024, 2, 29))
        datetime.datetime(2024, 2, 29, 0, 0)
        >>> last_dom(datetime(2024, 1, 31) + relativedelta(months=1))
        datetime.datetime(2024, 2, 29, 0, 0)
        >>> last_dom(datetime(2024, 2, 29) + relativedelta(months=1))
        datetime.datetime(2024, 3, 31, 0, 0)
    """
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = dt.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)


def last_doq(dt: datetime) -> datetime:
    """Get the latest day of quarter that relate with an input datetime value.
    :param dt:
    :return:

    Examples:
        >>> last_doq(datetime(2024, 2, 16))
        datetime.datetime(2024, 3, 31, 0, 0)
        >>> last_doq(datetime(2024, 12, 31))
        datetime.datetime(2024, 12, 31, 0, 0)
        >>> last_doq(datetime(2024, 8, 1))
        datetime.datetime(2024, 9, 30, 0, 0)
        >>> last_doq(datetime(2024, 9, 30))
        datetime.datetime(2024, 9, 30, 0, 0)
    """
    candidates: list[datetime] = [
        datetime(dt.year - 1, 12, 31, 0),
        datetime(dt.year, 3, 31, 0),
        datetime(dt.year, 6, 30, 0),
        datetime(dt.year, 9, 30, 0),
        datetime(dt.year, 12, 31, 0),
    ]
    return first(candidates, condition=lambda x: x >= dt)


def next_date_freq(dt: datetime, freq: str, prev: bool = False) -> datetime:
    """Prepare datetime to next datetime with frequency value.

    :param dt:
    :param freq:
    :param prev:
    :rtype: datetime

    Examples:
        >>> next_date_freq(datetime(2024, 1, 3), freq='D')
        datetime.datetime(2024, 1, 4, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 3), freq='D', prev=True)
        datetime.datetime(2024, 1, 2, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 3), freq='W')
        datetime.datetime(2024, 1, 10, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 3), freq='W', prev=True)
        datetime.datetime(2023, 12, 27, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 3), freq='M')
        datetime.datetime(2024, 2, 3, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 31), freq='M')
        datetime.datetime(2024, 2, 29, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 17), freq='Q')
        datetime.datetime(2024, 4, 17, 0, 0)
        >>> next_date_freq(datetime(2024, 1, 31), freq='Q')
        datetime.datetime(2024, 4, 30, 0, 0)
        >>> next_date_freq(datetime(2025, 12, 31), freq='Q')
        datetime.datetime(2026, 3, 31, 0, 0)
        >>> next_date_freq(datetime(2024, 5, 21), freq='Y')
        datetime.datetime(2025, 5, 21, 0, 0)
        >>> next_date_freq(datetime(2024, 5, 31), freq='Y')
        datetime.datetime(2025, 5, 31, 0, 0)
        >>> next_date_freq(datetime(2024, 5, 31), freq='Y', prev=True)
        datetime.datetime(2023, 5, 31, 0, 0)
    """
    if relativedelta is None:
        raise ImportError(
            "This function require `relativedelta` from the dateutil package, "
            "you should install with `pip install ddeutil[dateutil]`"
        )
    assert freq in ("D", "W", "M", "Q", "Y")
    operator: int = -1 if prev else 1
    if freq == "W":
        return dt + timedelta(days=7 * operator)
    elif freq == "M":
        if dt == last_dom(dt):
            return last_dom(dt + relativedelta(months=1 * operator))
        return dt + relativedelta(months=1 * operator)
    elif freq == "Q":
        if dt == last_dom(dt):
            return last_dom(dt + relativedelta(months=3 * operator))
        return dt + relativedelta(months=3 * operator)
    elif freq == "Y":
        if dt == last_dom(dt):
            return last_dom(dt + relativedelta(years=1 * operator))
        return dt + relativedelta(years=1 * operator)
    return dt + timedelta(days=1 * operator)


def calc_date_freq(dt: datetime, freq: str) -> datetime:
    """Prepare datetime to calculate datetime with frequency value.

    :param dt:
    :param freq:
    :rtype: datetime

        Examples:
            >>> calc_date_freq(datetime(2024, 1, 13), freq='D')
            datetime.datetime(2024, 1, 13, 0, 0)
            >>> calc_date_freq(datetime(2024, 1, 3), freq='W')
            datetime.datetime(2024, 1, 3, 0, 0)
            >>> calc_date_freq(datetime(2024, 1, 3), freq='M')
            datetime.datetime(2023, 12, 31, 0, 0)
            >>> calc_date_freq(datetime(2024, 1, 31), freq='M')
            datetime.datetime(2024, 1, 31, 0, 0)
            >>> calc_date_freq(datetime(2024, 1, 31), freq='Q')
            datetime.datetime(2023, 12, 31, 0, 0)
            >>> calc_date_freq(datetime(2025, 12, 31), freq='Q')
            datetime.datetime(2025, 12, 31, 0, 0)
            >>> calc_date_freq(datetime(2024, 12, 31), freq='Y')
            datetime.datetime(2024, 12, 31, 0, 0)
            >>> calc_date_freq(datetime(2024, 5, 31), freq='Y')
            datetime.datetime(2023, 12, 31, 0, 0)
    """
    if relativedelta is None:
        raise ImportError(
            "This function require relativedelta from the dateutil package, "
            "you should install with `pip install ddeutil[dateutil]`"
        )
    assert freq in ("D", "W", "M", "Q", "Y")
    if freq == "M":
        if dt != last_dom(dt):
            return last_dom(dt) - relativedelta(months=1)
        return dt
    elif freq == "Q":
        if dt != last_doq(dt):
            return last_dom(last_doq(dt) - relativedelta(months=3))
        return dt
    elif freq == "Y":
        if dt != dt.replace(month=12, day=31):
            return dt.replace(month=12, day=31) - relativedelta(years=1)
        return dt
    return dt


def calc_time_units(
    start_dt: datetime, end_dt: datetime, binding_days: bool = True
) -> tuple[Optional[str], Union[float, int]]:
    """Calculate time difference and return the primary unit type and value.

    :param start_dt: (datetime)
    :param end_dt: (datetime)
    :param binding_days: (bool)
    """
    rdelta = relativedelta(end_dt, start_dt)

    # NOTE: Check in order of precedence: years, months, hours, minutes
    if rdelta.years != 0:
        return "years", rdelta.years
    elif rdelta.months != 0 or rdelta.years != 0:
        return "months", rdelta.years * 12 + rdelta.months
    else:
        # NOTE: For days, hours and minutes, use total seconds for accuracy
        total_seconds: float = (end_dt - start_dt).total_seconds()

        # NOTE: 86400 seconds in a day
        total_days = int(total_seconds // 86400)
        total_hours = int(total_seconds // 3600)
        total_minutes = int(total_seconds // 60)

        if total_days != 0 and not binding_days:
            return "days", total_days
        elif total_hours != 0:
            return "hours", total_hours
        elif total_minutes != 0:
            return "minutes", total_minutes
        else:
            return None, 0


def gen_date_range(
    start_dt: datetime,
    end_dt: datetime,
    freq: FrequencyMode,
) -> list[datetime]:
    """Generate a list of datetime objects between start and end with given frequency"""
    if start_dt > end_dt:
        return []

    dates: list[datetime] = []
    current: datetime = start_dt

    if freq.endswith("D"):
        delta = timedelta(days=int(freq[:-1]))
    elif freq.endswith("H"):
        delta = timedelta(hours=int(freq[:-1]))
    elif freq.endswith("T"):
        delta = timedelta(minutes=int(freq[:-1]))
    else:
        raise ValueError(f"Unsupported frequency: {freq}")

    while current <= end_dt:
        dates.append(current)
        current += delta

    return dates


def get_date_range(
    start: Union[str, datetime],
    end: Union[str, datetime],
    execution_step: int = 1,
    execution_offset: int = 0,
    freq: Optional[FrequencyMode] = None,
    freq_step: int = 1,
    binding_days: bool = True,
) -> list[datetime]:
    """Get datetime range with date intervals

    :param start: (str | datetime)
    :param end: (str | datetime)
    :param execution_step: (int)
    :param execution_offset: (int)
    :param freq:
    :param freq_step: (int)
    :param binding_days:

    Note:
        The date range will force to daily for the maximum generator.
    """
    start_dt: datetime = parse_dt(start)
    end_dt: datetime = parse_dt(end)
    if freq:
        if freq not in FREQUENCY_SET:
            raise ValueError(f"Frequency, {freq!r}, does not support.")

        range_freq: FrequencyMode = "1D" if freq in ["1Y", "1M"] else freq
        min_dt, max_dt = min(start_dt, end_dt), max(start_dt, end_dt)
        return gen_date_range(min_dt, max_dt, range_freq)

    # Calculate new start and end based on unit type
    time_unit, time_value = calc_time_units(
        start_dt, end_dt, binding_days=binding_days
    )
    if time_unit is None:
        raise ValueError(f"Cannot find time difference between {start}, {end}")
    elif time_unit == "years":
        freq = f"{freq_step}Y"
        start_dt += relativedelta(years=time_value * execution_offset)
        end_dt = start_dt + relativedelta(years=time_value * execution_step)
    elif time_unit == "months":
        freq = f"{freq_step}M"
        start_dt += relativedelta(months=time_value * execution_offset)
        end_dt = start_dt + relativedelta(months=time_value * execution_step)
    elif time_unit == "days":
        freq = f"{freq_step}D"
        start_dt += relativedelta(days=time_value * execution_offset)
        end_dt = start_dt + relativedelta(days=time_value * execution_step)
    elif time_unit == "hours":
        freq = f"{freq_step}H"
        start_dt += relativedelta(hours=time_value * execution_offset)
        end_dt = start_dt + relativedelta(hours=time_value * execution_step)
    elif time_unit == "minutes":
        freq = f"{freq_step}T"
        start_dt += relativedelta(minutes=time_value * execution_offset)
        end_dt = start_dt + relativedelta(minutes=time_value * execution_step)
    else:
        raise ValueError(f"Time unit, {time_unit!r} does not support.")

    # NOTE: Convert frequency for date range generation
    #   (years/months use daily frequency).
    range_freq: FrequencyMode = "1D" if freq in ["1Y", "1M"] else freq
    min_dt, max_dt = min(start_dt, end_dt), max(start_dt, end_dt)
    return gen_date_range(min_dt, max_dt, range_freq)


def get_date_interval(
    start: Union[str, datetime],
    end: Union[str, datetime],
    execution_step: int = 1,
    execution_offset: int = 0,
    start_add_hours: int = 0,
    end_add_hours: int = 0,
    binding_days: bool = True,
) -> tuple[datetime, datetime]:
    """Get datetime interval with optional hour adjustments.

    :param start: (str | datetime)
    :param end: (str | datetime)
    :param execution_step: (int)
    :param execution_offset: (int)
    :param start_add_hours: (int)
    :param end_add_hours: (int)
    :param binding_days:
    """
    start_dt: datetime = parse_dt(start)
    end_dt: datetime = parse_dt(end)
    time_unit, time_value = calc_time_units(
        start_dt, end_dt, binding_days=binding_days
    )

    if time_unit is None:
        raise ValueError(f"Cannot find time difference between {start}, {end}")

    # NOTE: Calculate new start and end based on unit type
    if time_unit == "years":
        start_dt += relativedelta(years=time_value * execution_offset)
        end_dt = start_dt + relativedelta(years=time_value * execution_step)
    elif time_unit == "months":
        start_dt += relativedelta(months=time_value * execution_offset)
        end_dt = start_dt + relativedelta(months=time_value * execution_step)
    elif time_unit == "days":
        start_dt += relativedelta(days=time_value * execution_offset)
        end_dt = start_dt + relativedelta(days=time_value * execution_step)
    elif time_unit == "hours":
        start_dt += relativedelta(hours=time_value * execution_offset)
        end_dt = start_dt + relativedelta(hours=time_value * execution_step)
    elif time_unit == "minutes":
        start_dt += relativedelta(minutes=time_value * execution_offset)
        end_dt = start_dt + relativedelta(minutes=time_value * execution_step)

    # NOTE: Apply hour adjustments
    start_dt += relativedelta(hours=start_add_hours)
    end_dt += relativedelta(hours=end_add_hours)
    return min(start_dt, end_dt), max(start_dt, end_dt)
