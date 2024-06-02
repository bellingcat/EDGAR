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

def parse_location_input(location_input: str | tuple | None) -> str | None:
    """
    Handles text search input for --peo_in or --inc_in.

    This function processes the input to ensure it is in an acceptable format 
    for location searches. Because CLI input like --peo_in "NY, OH" yields
    python value ('NY','OH'), this function supports single or multiple locations 
    provided as a string or a tuple. If the input is a tuple, it converts the tuple 
    to a comma-separated string. It also removes any whitespace from the output 
    string to prevent errors during further processing. Also validates that all
    provided location codes are in the TEXT_SEARCH_LOCATIONS_MAPPING and prints
    the list of acceptable codes if not.

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
            f'peo_in and inc_in must use format like "NY" or "NY,OH,etc" '
            f'and be one of {TEXT_SEARCH_LOCATIONS_MAPPING}'
        )

    if isinstance(location_input, tuple):
        for value in location_input:
            if value not in TEXT_SEARCH_LOCATIONS_MAPPING:
                raise ValueError(f"{value} not in {TEXT_SEARCH_LOCATIONS_MAPPING}")
        location_input = ','.join(location_input)

    elif isinstance(location_input, str):
        if location_input not in TEXT_SEARCH_LOCATIONS_MAPPING:
            raise ValueError(f"{location_input} not in {TEXT_SEARCH_LOCATIONS_MAPPING}")

    if location_input:
        location_input = location_input.replace(" ", "")

    return location_input
