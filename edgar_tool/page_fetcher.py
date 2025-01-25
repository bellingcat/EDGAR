import time
import uuid
from random import uniform
from typing import Any, Callable, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(
    wait=wait_fixed(uniform(0.1, 0.15)),
    stop=stop_after_attempt(3),
    reraise=True,
)
def fetch_page(url: str) -> dict:
    """
    Fetches the given URL and retries the request if the page load fails.

    :param url: URL to fetch
    :param min_wait_seconds: minimum wait time for the request to complete before executing the check method
    :param max_wait_seconds: maximum wait time for the request to complete before executing the check method
    :param stop_after_n: how many times to retry the request before failing
    :return: wrapper function that takes a check method and retries the request if the page load fails
    """

    print(f"Requesting URL: {url}")
    headers = {
        "User-Agent": f"BellingcatEDGARTool_{uuid.uuid4()} contact-tech@bellingcat.com"
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise PageCheckFailedError(f"Error for url {url}, with code {res.status_code}")
    json_response = res.json()
    print(f"Successfully fetched URL: {url}")
    return json_response


class ResultsTableNotFoundError(Exception):
    pass


class PageCheckFailedError(Exception):
    pass


class NoResultsFoundError(Exception):
    pass
