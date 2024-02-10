from typing import Callable, Any


def none_when_error(func: Callable[..., Any]) -> Callable[..., Any]:
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
