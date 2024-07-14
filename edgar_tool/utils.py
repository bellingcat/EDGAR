from __future__ import annotations

import re
from datetime import date
from typing import Any, Iterator, Dict, List, Union, Optional
from edgar_tool.constants import TEXT_SEARCH_LOCATIONS_MAPPING


def split_date_range_in_n(start: date, end: date, n: int) -> Iterator[date]:
    """
    Generator returning a list of N dates at regular intervals between start and end dates

    :param start: start date to generate intervals from
    :param end: end date until which we should generate intervals
    :param n: number of intervals to generate
    :return:
    """
    diff = (end - start) / n
    for i in range(n):
        yield start + diff * i
    yield end


def safe_get(d: Dict, *keys) -> Any:
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


def invert_dict(d: dict) -> dict:
    """
    Returns an inverted dictionary such that values are keys and keys are values.
    If there are duplicate values, the last occurring key-value pair will prevail.
    """
    return {v: k for k, v in d.items()}


def replace_ignore_case_whitespace(s, location, replacement):
    """
    Perform a case-insensitive and whitespace-insensitive replacement of a substring in a string.

    Parameters:
    s (str): The original string.
    location (str): The substring to be replaced.
    replacement (str): The replacement substring.

    Returns:
    str: The modified string with the replacements made.
    """
    # Create a regex pattern that ignores whitespace and is case-insensitive
    location_pattern = re.compile(
        r"\s*".join(re.escape(char) for char in location), re.IGNORECASE
    )
    return location_pattern.sub(replacement, s)


def replace_substrings_in_string(s) -> str:
    """
    Takes a string like "New York, OH" and returns a string with the full
    location names converted to codes such as "NY,OH". Returns an unmodified
    string if there are no full location names present. Note that matching
    full location names shall be case and whitespace insensitive.

    Parameters:
    s (str): The original string.

    Returns:
    str: The modified string with substrings replaced.
    """
    locations2codes = invert_dict(TEXT_SEARCH_LOCATIONS_MAPPING)
    locations2codes = {
        k.replace(" ", "").lower(): v for k, v in locations2codes.items()
    }
    for location in locations2codes.keys():
        if location in s.replace(" ", "").lower():
            s = replace_ignore_case_whitespace(s, location, locations2codes[location])
    return s


def parse_location_input(location_input: str | tuple | None) -> str | None:
    """
    Handles text search input for --peo_in or --inc_in.

    This function processes the input to ensure it is in an acceptable format
    for location searches. Because CLI input like --peo_in "NY, OH" yields
    runtime value ('NY','OH'), this function supports single or multiple locations
    provided as a string or a tuple. If the input is a tuple, it converts the tuple
    to a comma-separated string. It also removes any whitespace from the output
    string to prevent errors during further processing. Also validates that all
    provided location codes are in the TEXT_SEARCH_LOCATIONS_MAPPING and prints
    the list of acceptable codes if not. If the input string is a location's full name
    instead of the code (i.e. 'New York' instead of 'NY'), then strings present in
    TEXT_SEARCH_LOCATIONS_MAPPING.values() are mapped to an code value instead.

    Parameters:
    location_input (str | tuple | None): The input location(s) to be parsed.
        It can be a single location as a string, multiple locations as a tuple
        of strings, or None.

    Returns:
    str: A string representation of the location(s) with no whitespace.

    Raises:
    ValueError: If the input is not a string, tuple, or None, or if any location
        in the input is not in the TEXT_SEARCH_LOCATIONS_MAPPING.
    """

    if not isinstance(location_input, (str, tuple, type(None))):
        raise ValueError(
            f'peo_in and inc_in must use format like "NY" or "NY,OH,etc"'
            f"and be one of {TEXT_SEARCH_LOCATIONS_MAPPING}"
        )
    if isinstance(location_input, tuple):
        location_input = ",".join(location_input)

    if isinstance(location_input, str):
        location_input = tuple(replace_substrings_in_string(location_input).split(","))
        for value in location_input:
            # Eliminate issues caused by casing and whitespaces
            value = value.replace(" ", "").upper()
            if value not in TEXT_SEARCH_LOCATIONS_MAPPING.keys():
                raise ValueError(f"{value} not in {TEXT_SEARCH_LOCATIONS_MAPPING}")
        location_input = ",".join(location_input)

    if location_input:
        location_input = location_input.replace(" ", "")

    return location_input
