from datetime import datetime

import pytest

from ..time import DateRange, SubDateRange, TimeResolution


@pytest.fixture
def date_ranges():
    dr1 = SubDateRange(datetime(2024, 1, 1), datetime(2024, 1, 5))
    dr2 = SubDateRange(datetime(2024, 1, 10), datetime(2024, 1, 15))
    dr3 = SubDateRange(datetime(2024, 1, 5), datetime(2024, 1, 10))
    dr4 = SubDateRange(datetime(2024, 1, 12), datetime(2024, 1, 20))
    return DateRange([dr1, dr2]), DateRange([dr3, dr4])


def test_add(date_ranges):
    ranges1, ranges2 = date_ranges
    combined = ranges1 + ranges2
    assert len(combined.ranges) == 3


@pytest.mark.parametrize(
    "date, expected",
    [
        (datetime(2024, 1, 3), True),
        (datetime(2024, 1, 8), False),
    ],
)
def test_contains(date_ranges, date, expected):
    ranges1, _ = date_ranges
    assert (date in ranges1) == expected


@pytest.mark.parametrize("expected_len", [1])
def test_intersection(date_ranges, expected_len):
    ranges1, ranges2 = date_ranges
    intersections = ranges1.intersection(ranges2)
    assert len(intersections.ranges) == expected_len


@pytest.mark.parametrize("expected_len", [1])
def test_gaps(date_ranges, expected_len):
    ranges1, _ = date_ranges
    gaps = ranges1.gaps()
    assert len(gaps.ranges) == expected_len


@pytest.mark.parametrize(
    "expected_start, expected_end",
    [
        (datetime(2024, 1, 1), datetime(2024, 1, 15)),
    ],
)
def test_union(date_ranges, expected_start, expected_end):
    ranges1, _ = date_ranges
    union_range = ranges1.union()
    assert union_range.lstart == expected_start
    assert union_range.rend == expected_end


def test_time_resolution():
    res = ["raw", "minute", "hour", "day", "week", "month", "year"]
    for i, ri in enumerate(res):
        for j, rj in enumerate(res):
            assert (i < j) == (TimeResolution(ri) > TimeResolution(rj))

    assert TimeResolution("raw").pandas_alias is None
    assert TimeResolution("minute").pandas_alias == "5T"
    assert TimeResolution("hour").pandas_alias == "H"
    assert TimeResolution("day").pandas_alias == "D"
