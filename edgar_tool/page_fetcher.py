import time
import uuid
from random import uniform
from typing import Any, Callable, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(
    before=wait_fixed(
        0.11
    ),  # The SEC API limits us to max 10 requests per second. Let's be conservative.
    stop=stop_after_attempt(3),
    reraise=True,
)
def fetch_page(url: str) -> dict:
    """
    Fetches the given URL and retries the request if the page load fails.

    :param url: URL to fetch
    :return: JSON response from the URL
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
