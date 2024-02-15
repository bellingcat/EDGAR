from datetime import date
from typing import Callable, Any, Iterator


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


def try_or_none(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that returns None when an exception occurs in the decorated function.

    :param func: Function to decorate
    :return: Decorated function
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(
                f"Function {func.__name__} raised a {e.__class__.__name__} error with message: {e}"
            )
            print(f"Returning None...")
            return None

    return wrapper
