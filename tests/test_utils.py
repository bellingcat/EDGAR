import datetime

import pytest

from edgar_tool.utils import split_date_range_in_half


def test_split_date_range_in_half_when_dates_are_beginning_and_end_of_month():
    # GIVEN
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 31)
    iterator = split_date_range_in_half(start_date, end_date)

    # WHEN
    first_date, second_date = next(iterator)
    third_date, fourth_date = next(iterator)

    # THEN
    assert first_date, second_date == (
        datetime.date(2024, 1, 1),
        datetime.date(2024, 1, 16),
    )
    assert third_date, fourth_date == (
        datetime.date(2024, 1, 17),
        datetime.date(2024, 1, 31),
    )


def test_split_date_range_in_half_when_dates_are_next_to_each_other():
    # GIVEN
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 2)
    iterator = split_date_range_in_half(start_date, end_date)

    # WHEN
    first_date, second_date = next(iterator)
    third_date, fourth_date = next(iterator)

    # THEN
    assert first_date, second_date == (
        datetime.date(2024, 1, 1),
        datetime.date(2024, 1, 1),
    )
    assert third_date, fourth_date == (
        datetime.date(2024, 1, 2),
        datetime.date(2024, 1, 2),
    )


def test_split_date_range_in_half_when_dates_are_same():
    # GIVEN
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 1)
    expected_error_message = (
        "Cannot split dates when both start and end dates are "
        "the same. SEC API does not support half days."
    )

    # WHEN / THEN
    with pytest.raises(ValueError, match=expected_error_message):
        next(split_date_range_in_half(start_date, end_date))
