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

def invert_dict(d:dict)->dict:
    """
        Returns an inverted dictionary such that values are keys and keys are values.
        If there are duplicate values, the last occurring key-value pair will prevail. 
    """
    return {v: k for k, v in d.items()}

def replace_substrings_in_string(s):
    """
    Takes a string like "New York, OH" and returns a string with the full 
    location names converted to codes such as "NY, OH". Returns an unmodified 
    string if there are no location names present. Note that white strings are
    removed and all letters are converted to lowercase to avoid unwanted string mismatches. 

    Parameters:
    s (str): The original string.

    Returns:
    str: The modified string with substrings replaced.
    """
    locations2codes = invert_dict(TEXT_SEARCH_LOCATIONS_MAPPING)
    locations2codes = {k.replace(" ", "").lower(): v for k, v in locations2codes.items()}
    s = s.replace(" ", "").lower()
    for location in locations2codes.keys():
        if location in s:
            s = s.replace(location, locations2codes[location])
    return s.upper()
    

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
            f'and be one of {TEXT_SEARCH_LOCATIONS_MAPPING}'
        )
    if isinstance(location_input,tuple):
        location_input = ','.join(location_input)
    
    if isinstance(location_input,str):
        ## regardless of input format, convert to tup because --peo_in "New York, OH" is interpreted as a string
        location_input = tuple(replace_substrings_in_string(location_input).split(','))
        for value in location_input:
            if value not in TEXT_SEARCH_LOCATIONS_MAPPING and value not in TEXT_SEARCH_LOCATIONS_MAPPING.values():
                raise ValueError(f"{value} not in {TEXT_SEARCH_LOCATIONS_MAPPING}")
        location_input = ','.join(location_input)

    if location_input:
        location_input = location_input.replace(" ", "")
        
    return location_input
