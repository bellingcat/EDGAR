import time
import uuid
from random import uniform
from typing import Any, Callable, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


def fetch_page(
    url: str,
    min_wait_seconds: float,
    max_wait_seconds: float,
    stop_after_n: int,
) -> Callable[[Callable[..., Any], Optional[str]], None]:
    """
    Curried function that fetches the given URL and retries the request if the page load fails.
    Example usage: fetch_page(driver, url, 10, 3)(lambda: driver.find_element(By.ID, 'foo').text != "failed")

    :param url: URL to fetch
    :param min_wait_seconds: minimum wait time for the request to complete before executing the check method
    :param max_wait_seconds: maximum wait time for the request to complete before executing the check method
    :param stop_after_n: how many times to retry the request before failing
    :return: wrapper function that takes a check method and retries the request if the page load fails
    """

    @retry(
        wait=wait_fixed(uniform(min_wait_seconds, max_wait_seconds)),
        stop=stop_after_attempt(stop_after_n),
        reraise=True,
    )
    def wrapper(check_method: Callable, err_msg: Optional[str] = None) -> None:
        print(f"Requesting URL: {url}")
        headers = {
            "User-Agent": f"BellingcatEDGARTool_{uuid.uuid4()} contact-tech@bellingcat.com"
        }
        res = requests.get(url, headers=headers)
        randomized_wait = uniform(min_wait_seconds, max_wait_seconds)
        print(f"Waiting {randomized_wait} seconds for the request to complete...")
        time.sleep(randomized_wait)
        if res.status_code != 200:
            raise PageCheckFailedError(
                err_msg or f"Error for url {url}, with code {res.status_code}"
            )
        json_response = res.json()
        if not check_method(json_response):
            raise PageCheckFailedError(err_msg or f"Page check failed for url {url}")
        print(f"Successfully fetched URL: {url}")
        return json_response

    return wrapper


class ResultsTableNotFoundError(Exception):
    pass


class PageCheckFailedError(Exception):
    pass


class NoResultsFoundError(Exception):
    pass
