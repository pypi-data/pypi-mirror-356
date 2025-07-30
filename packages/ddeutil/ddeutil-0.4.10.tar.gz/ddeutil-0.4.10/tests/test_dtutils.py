from datetime import date, datetime, timedelta, timezone
from unittest import mock
from zoneinfo import ZoneInfo

import ddeutil.core.dtutils as dtutils
import pytest
from dateutil.relativedelta import relativedelta
from ddeutil.core.dtutils import (
    DatetimeDim,
    calc_date_freq,
    calc_time_units,
    closest_quarter,
    gen_date_range,
    get_date_interval,
    get_date_range,
    last_dom,
    next_date,
    next_date_freq,
    parse_dt,
    parse_dt_default,
)
from freezegun import freeze_time


def test_parse_datetime_str():
    assert parse_dt_default(date(2024, 1, 1)) == datetime(2024, 1, 1, 0)
    assert parse_dt_default(datetime(2024, 1, 1)) == datetime(2024, 1, 1, 0)
    assert parse_dt_default("2024-01-01") == datetime(2024, 1, 1, 0)
    assert parse_dt_default("2024-01-01 00:00:00") == datetime(2024, 1, 1, 0)
    assert parse_dt_default("2024-01-01 00:00:00.00") == datetime(2024, 1, 1, 0)
    assert parse_dt_default("2024-01-01T00:00:00Z") == datetime(
        2024, 1, 1, 0, tzinfo=timezone.utc
    )
    assert parse_dt_default("2024-01-01 15:30:00+05:00") == datetime(
        2024, 1, 1, 15, 30, tzinfo=timezone(timedelta(seconds=18000))
    )
    assert parse_dt_default("2024-01-01T15:30:00-05:00") == datetime(
        2024, 1, 1, 15, 30, tzinfo=timezone(timedelta(seconds=-18000))
    )

    with pytest.raises(ValueError):
        parse_dt_default(123)

    with pytest.raises(ValueError):
        parse_dt_default("123")


def test_parse_dt():
    assert parse_dt_default(date(2024, 1, 1)) == datetime(2024, 1, 1, 0)
    assert parse_dt_default(datetime(2024, 1, 1)) == datetime(2024, 1, 1, 0)
    assert parse_dt("2024-01-01") == datetime(2024, 1, 1, 0)
    assert parse_dt("01 Jan 2024") == datetime(2024, 1, 1, 0)
    assert parse_dt("20240101") == datetime(2024, 1, 1, 0)
    assert parse_dt("2024 Jan Monday") == datetime(2024, 1, 22, 0)
    assert parse_dt("2024-01-01 00:00:00") == datetime(2024, 1, 1, 0)
    assert parse_dt("2024-01-01 15:00:00 BKK") == datetime(2024, 1, 1, 15)
    assert parse_dt(
        "2024-01-01 15:00:00 BKK", tzinfos={"BKK": ZoneInfo("Asia/Bangkok")}
    ) == datetime(2024, 1, 1, 15, tzinfo=ZoneInfo("Asia/Bangkok"))
    assert parse_dt("2024-01-01 15:00:00 UTC") == datetime(
        2024, 1, 1, 15, tzinfo=timezone.utc
    )
    assert parse_dt("2024-01-01 15:00:00 +07:00") == datetime(
        2024, 1, 1, 15, tzinfo=timezone(timedelta(seconds=25200))
    )
    assert parse_dt("2024-01-01 15:00:00 +00:00") == datetime(
        2024, 1, 1, 15, tzinfo=timezone.utc
    )
    assert parse_dt("01 Jan 2024 15:00:00 +00") == datetime(
        2024, 1, 1, 15, tzinfo=timezone.utc
    )


def test_dt_dimension():
    assert 6 == DatetimeDim.get_dim("year")

    with pytest.raises(ValueError):
        DatetimeDim.get_dim("date_of_month")


def test_get_date():
    assert datetime.now(tz=dtutils.LOCAL_TZ).date() == dtutils.get_date("date")

    with freeze_time("2024-01-01 01:00:00"):
        assert datetime(
            2024,
            1,
            1,
            1,
        ).replace(
            tzinfo=dtutils.LOCAL_TZ
        ) == dtutils.get_date("datetime", _tz=dtutils.LOCAL_TZ)

        assert datetime(
            2024,
            1,
            1,
            1,
        ).replace(
            tzinfo=dtutils.LOCAL_TZ
        ) == dtutils.get_date("datetime", _tz="UTC")

        assert "20240101010000" == dtutils.get_date("%Y%m%d%H%M%S")


def test_next_date():
    with mock.patch("ddeutil.core.dtutils.relativedelta", None):
        with pytest.raises(ImportError):
            next_date(datetime(2024, 1, 1), mode="day")

    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="day") == datetime(
        2023, 2, 1, 0, 0
    )
    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="month") == datetime(
        2023, 2, 28, 0, 0
    )
    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="hour") == datetime(
        2023, 1, 31, 1, 0
    )
    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="year") == datetime(
        2024, 1, 31, 0, 0
    )


def test_closest_quarter():
    assert closest_quarter(datetime(2024, 9, 25)) == datetime(2024, 9, 30, 0, 0)
    assert closest_quarter(datetime(2024, 2, 13)) == datetime(
        2023, 12, 31, 0, 0
    )


def test_last_dom():
    assert last_dom(datetime(2024, 2, 29)) == datetime(2024, 2, 29, 0, 0)
    assert last_dom(
        datetime(2024, 1, 31) + relativedelta(months=1)
    ) == datetime(2024, 2, 29, 0, 0)
    assert last_dom(
        datetime(2024, 2, 29) + relativedelta(months=1)
    ) == datetime(2024, 3, 31, 0, 0)


def test_replace_date():
    assert datetime(2023, 1, 31, 0, 0) == dtutils.replace_date(
        datetime(2023, 1, 31, 13, 2, 47),
        mode="day",
    )

    assert datetime(2023, 1, 1, 0, 0) == dtutils.replace_date(
        datetime(2023, 1, 31, 13, 2, 47),
        mode="year",
    )


def test_next_date_freq():
    assert next_date_freq(datetime(2024, 1, 3), freq="D") == datetime(
        2024, 1, 4, 0, 0
    )
    assert next_date_freq(
        datetime(2024, 1, 3), freq="D", prev=True
    ) == datetime(2024, 1, 2, 0, 0)
    assert next_date_freq(datetime(2024, 1, 3), freq="W") == datetime(
        2024, 1, 10, 0, 0
    )
    assert next_date_freq(
        datetime(2024, 1, 3), freq="W", prev=True
    ) == datetime(2023, 12, 27, 0, 0)
    assert next_date_freq(datetime(2024, 1, 3), freq="M") == datetime(
        2024, 2, 3, 0, 0
    )
    assert next_date_freq(datetime(2024, 1, 31), freq="M") == datetime(
        2024, 2, 29, 0, 0
    )
    assert next_date_freq(datetime(2024, 1, 17), freq="Q") == datetime(
        2024, 4, 17, 0, 0
    )
    assert next_date_freq(datetime(2024, 1, 31), freq="Q") == datetime(
        2024, 4, 30, 0, 0
    )
    assert next_date_freq(datetime(2025, 12, 31), freq="Q") == datetime(
        2026, 3, 31, 0, 0
    )
    assert next_date_freq(datetime(2024, 5, 21), freq="Y") == datetime(
        2025, 5, 21, 0, 0
    )
    assert next_date_freq(datetime(2024, 5, 31), freq="Y") == datetime(
        2025, 5, 31, 0, 0
    )
    assert next_date_freq(
        datetime(2024, 5, 31), freq="Y", prev=True
    ) == datetime(2023, 5, 31, 0, 0)

    with mock.patch("ddeutil.core.dtutils.relativedelta", None):
        with pytest.raises(ImportError):
            next_date_freq(datetime(2024, 5, 31), freq="Y", prev=True)


def test_calc_data_freq():
    assert calc_date_freq(datetime(2024, 1, 13), freq="D") == datetime(
        2024, 1, 13, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 3), freq="W") == datetime(
        2024, 1, 3, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 3), freq="M") == datetime(
        2023, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 31), freq="M") == datetime(
        2024, 1, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 31), freq="Q") == datetime(
        2023, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2025, 12, 31), freq="Q") == datetime(
        2025, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 12, 31), freq="Y") == datetime(
        2024, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 5, 31), freq="Y") == datetime(
        2023, 12, 31, 0, 0
    )

    with mock.patch("ddeutil.core.dtutils.relativedelta", None):
        with pytest.raises(ImportError):
            calc_date_freq(datetime(2024, 5, 31), freq="Y")


def test_get_date_interval():
    start, end = get_date_interval(
        "2024-12-25 20:00:00", "2024-12-26 20:00:00", 1, 1
    )
    assert start == datetime(2024, 12, 26, 20)
    assert end == datetime(2024, 12, 27, 20)

    start, end = get_date_interval(
        "2024-12-25 20:00:00", "2024-12-26 20:00:00", -3, 1
    )
    assert start == datetime(2024, 12, 23, 20)
    assert end == datetime(2024, 12, 26, 20)

    with pytest.raises(ValueError):
        get_date_interval(datetime(2024, 1, 1), datetime(2024, 1, 1))

    assert get_date_interval(
        datetime(2024, 1, 1), datetime(2025, 1, 1), 1, 1
    ) == (datetime(2025, 1, 1, 0, 0), datetime(2026, 1, 1, 0, 0))
    assert get_date_interval(
        datetime(2024, 1, 1), datetime(2024, 2, 12), 1, 1
    ) == (datetime(2024, 2, 1, 0, 0), datetime(2024, 3, 1, 0, 0))

    assert get_date_interval(
        "2024-12-25 20:00:00", "2024-12-25 20:15:00", 1, 1
    ) == (datetime(2024, 12, 25, 20, 15), datetime(2024, 12, 25, 20, 30))

    assert get_date_interval(
        "2024-12-01 00:00:00", "2024-12-15 00:00:00", 1, 1, binding_days=False
    ) == (datetime(2024, 12, 15, 00, 0), datetime(2024, 12, 29, 00, 0))

    assert get_date_interval(
        "2024-11-01 00:00:00", "2024-12-15 00:00:00", 1, 0
    ) == (datetime(2024, 11, 1, 00, 0), datetime(2024, 12, 1, 00, 0))


def test_gen_date_range():
    assert (
        gen_date_range(datetime(2024, 1, 2), datetime(2024, 1, 1), "1D") == []
    )

    with pytest.raises(ValueError):
        gen_date_range(datetime(2024, 1, 1), datetime(2024, 1, 4), "1Q")


def test_get_date_range():
    assert get_date_range(
        datetime(2024, 1, 1), datetime(2024, 1, 8), binding_days=False
    ) == [
        datetime(2024, 1, 1),
        datetime(2024, 1, 2),
        datetime(2024, 1, 3),
        datetime(2024, 1, 4),
        datetime(2024, 1, 5),
        datetime(2024, 1, 6),
        datetime(2024, 1, 7),
        datetime(2024, 1, 8),
    ]
    assert get_date_range(
        datetime(2024, 1, 1, 18), datetime(2024, 1, 8), binding_days=False
    ) == [
        datetime(2024, 1, 1, 18),
        datetime(2024, 1, 2, 18),
        datetime(2024, 1, 3, 18),
        datetime(2024, 1, 4, 18),
        datetime(2024, 1, 5, 18),
        datetime(2024, 1, 6, 18),
        datetime(2024, 1, 7, 18),
    ]
    assert get_date_range(
        datetime(2024, 1, 1, 18), datetime(2024, 1, 2), freq="1D"
    ) == [datetime(2024, 1, 1, 18)]

    assert get_date_range(datetime(2024, 1, 1, 18), datetime(2024, 1, 2)) == [
        datetime(2024, 1, 1, 18),
        datetime(2024, 1, 1, 19),
        datetime(2024, 1, 1, 20),
        datetime(2024, 1, 1, 21),
        datetime(2024, 1, 1, 22),
        datetime(2024, 1, 1, 23),
        datetime(2024, 1, 2),
    ]

    assert get_date_range(
        datetime(2024, 1, 1, 9), datetime(2024, 2, 1), binding_days=False
    ) == [
        # NOTE: Generate datetime from day 1 to day 31
        datetime(2024, 1, r, 9)
        for r in range(1, 32)
    ]

    assert get_date_range(
        datetime(2024, 1, 1, 7, 1), datetime(2024, 1, 1, 7, 5)
    ) == [
        datetime(2024, 1, 1, 7, 1),
        datetime(2024, 1, 1, 7, 2),
        datetime(2024, 1, 1, 7, 3),
        datetime(2024, 1, 1, 7, 4),
        datetime(2024, 1, 1, 7, 5),
    ]

    assert (
        len(get_date_range(datetime(2024, 1, 1), datetime(2025, 1, 1))) == 367
    )
    assert (
        len(get_date_range(datetime(2024, 1, 1), datetime(2024, 2, 12))) == 32
    )

    # NOTE: Raise because freq value does not support.
    with pytest.raises(ValueError):
        get_date_range(
            datetime(2024, 1, 1, 18), datetime(2024, 1, 2), freq="1Q"
        )

    with pytest.raises(ValueError):
        get_date_range(datetime(2024, 1, 1), datetime(2024, 1, 1), freq="1D")

    with pytest.raises(ValueError):
        get_date_range(datetime(2024, 1, 1), datetime(2024, 1, 1))


def test_calc_time_units():
    """Test calculating year differences"""
    unit, value = calc_time_units(datetime(2024, 1, 1), datetime(2026, 1, 1))
    assert unit == "years"
    assert value == 2

    unit, value = calc_time_units(datetime(2024, 1, 1), datetime(2024, 4, 1))
    assert unit == "months"
    assert value == 3

    unit, value = calc_time_units(
        datetime(2024, 1, 1), datetime(2024, 1, 8), binding_days=False
    )
    assert unit == "days"
    assert value == 7

    unit, value = calc_time_units(
        datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 15, 0)
    )
    assert unit == "hours"
    assert value == 5

    unit, value = calc_time_units(
        datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 10, 30)
    )
    assert unit == "minutes"
    assert value == 30

    unit, value = calc_time_units(
        datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 10, 0)
    )
    assert unit is None
    assert value == 0
