from datetime import date
from typing import Callable, Any, Iterator, Dict, TypeVar, Optional, List

from selenium.webdriver.remote.webelement import WebElement


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


T = TypeVar("T")


def safe_func(
    func: Callable[..., T], default: Optional[T] = None
) -> Callable[..., Optional[T]]:
    """
    Decorator that returns None when an exception occurs in the decorated function.

    :param func: Function to decorate
    :param default: Default value to return when an exception occurs
    :return: Decorated function
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(
                f"Function {func.__name__} raised a {e.__class__.__name__} error, returning {default}: {e}"
            )
            return default

    return wrapper


def split_html_by_line(element: WebElement) -> List[str]:
    """
    Handles line breaks in the given WebElement's innerHTML attribute.
    This fixes an issue due to innerText trimming line breaks.

    :param element: WebElement to handle line breaks for
    :return: InnerHTML with line breaks replaced by a space
    """

    return element.get_attribute("innerHTML").split("<br>")
