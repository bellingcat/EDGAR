from __future__ import annotations

from datetime import date
from typing import Any, Iterator, List, Optional, Union


def split_date_range_in_half(start: date, end: date) -> Iterator[date, date]:
    """
    Generator returning a list of N dates at regular intervals between start and end dates

    :param start: start date to generate intervals from
    :param end: end date until which we should generate intervals
    :param n: number of intervals to generate
    :yield: iterator of tuples of two dates
    """
    if start == end:
        raise ValueError(
            "Cannot split dates when both start and end dates are the same. SEC API does not support half days."
        )
    diff = (end - start) / 2
    yield start, start + diff
    yield start + diff, end


def safe_get(d: dict, *keys) -> Any:
    """
    Safely get a value from a nested dictionary without raising a KeyError

    :param d: Dictionary to get the value from
    :param keys: Keys to traverse the dictionary
    :return: Value at the given keys, or None if the keys are not found
    """
    for key in keys:
        try:
            d = d[key]
        except KeyError:
            return None
    return d


def unpack_singleton_list(l: Optional[List]) -> Union[str, List[str]]:
    return l if (l is None) or (len(l) != 1) else l[0]
