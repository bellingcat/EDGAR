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

def parse_location_input(location_input: str | tuple | None) -> str:
    """
    Handles text search input for --peo_in or --inc_in.
    
    If the input is a full location name, it converts it to its corresponding code 
    (e.g., "Sierra Leone" => "T8"). If the input is multiple locations, it converts 
    the tuple to a string representation of a list. This function removes whitespace 
    from the output string, which can cause additional locations to be ignored. It raises 
    a ValueError if the locations are not of the accepted types.
    """
    
    if not isinstance(location_input, (str, tuple, type(None))):
        raise ValueError(
            f'peo_in and inc_in must use format like "NY" or "NY,OH,etc" '
            f'and be one of {list(TEXT_SEARCH_LOCATIONS_MAPPING.keys())}'
        )

    name2code = {value: key for key, value in TEXT_SEARCH_LOCATIONS_MAPPING.items()}

    if isinstance(location_input, tuple):
        location_input = tuple(
            name2code.get(value, value)  
            for value in location_input
        )
        for value in location_input:
            if value not in TEXT_SEARCH_LOCATIONS_MAPPING:
                raise ValueError(f"{value} not in {list(TEXT_SEARCH_LOCATIONS_MAPPING.keys())}")
        location_input = ','.join(location_input)
        
    elif isinstance(location_input, str):
        if location_input in TEXT_SEARCH_LOCATIONS_MAPPING.values():
            location_input = name2code[location_input]
        elif location_input not in TEXT_SEARCH_LOCATIONS_MAPPING.keys():
            raise ValueError(f"{location_input} not in {list(TEXT_SEARCH_LOCATIONS_MAPPING.keys())}")

    if location_input:
        location_input = location_input.replace(" ","")
        
    return location_input