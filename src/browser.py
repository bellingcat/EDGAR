import sys
import time
from contextlib import contextmanager
from typing import Union, Callable, Any, List, Dict, Iterator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver as EdgeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.ie.webdriver import WebDriver as IeWebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from tenacity import retry, wait_fixed, stop_after_attempt
from fake_useragent import UserAgent

BrowserDriver = Union[
    ChromeWebDriver, SafariWebDriver, FirefoxWebDriver, EdgeWebDriver, IeWebDriver
]

CHROME = "chrome"
SAFARI = "safari"
FIREFOX = "firefox"
EDGE = "edge"

ACCEPTED_BROWSERS = [CHROME, SAFARI, FIREFOX, EDGE]


def fetch_page(
    driver: BrowserDriver,
    url: str,
    wait_for_request_secs: int,
    stop_after_n: int,
) -> Callable[[Callable[..., Any]], None]:
    """
    Curried function that fetches the given URL and retries the request if the page load fails.
    Example usage: fetch_page(driver, url, 10, 3)(lambda: driver.find_element(By.ID, 'foo').text != "failed")

    :param driver: Selenium WebDriver
    :param url: URL to fetch
    :param wait_for_request_secs: how long to wait for the request to complete before executing the check method
    :param stop_after_n: how many times to retry the request before failing
    :return: wrapper function that takes a check method and retries the request if the page load fails
    """

    @retry(
        wait=wait_fixed(wait_for_request_secs),
        stop=stop_after_attempt(stop_after_n),
        reraise=True,
    )
    def wrapper(check_method: Callable) -> None:
        print(f"Requesting URL: {url}")
        driver.get(url)
        print(
            f"Waiting {wait_for_request_secs} seconds for the request to complete..."
        )
        time.sleep(wait_for_request_secs)
        if not check_method():
            raise PageCheckFailedError(
                "Page check failed, page load seems to have failed"
            )
        print(f"Successfully fetched URL: {url}")

    return wrapper


def extract_html_table_rows(
    driver: BrowserDriver, by: str, table_body_selector: str
) -> Callable[
    [Callable[[List[WebElement]], List[Dict[str, Any]]]], Iterator[Dict[str, Any]]
]:
    """
    Curried function that extracts the rows of an HTML table and parses them into a list of dictionaries.
    Example usage: extract_html_table_rows(driver, By.XPATH, "/html/body/div[1]/table/tbody")(parse_table_rows)

    :param driver: Selenium WebDriver
    :param by: Selenium By method to use for finding the table body
    :param table_body_selector: Selector for the table body
    :return: wrapper function that takes a parse method and returns the parsed table rows
    """

    def wrapper(
        parse_func: Callable[[List[WebElement]], List[Dict[str, Any]]]
    ) -> Iterator[Dict[str, Any]]:
        table_body = driver.find_element(by, table_body_selector)
        if table_body is None:
            raise ResultsTableNotFoundError(
                "Results table body not found, page load seems to have failed"
            )

        rows: List[WebElement] = table_body.find_elements(By.TAG_NAME, "tr")
        print(f"Fetched {len(rows)} rows")

        parsed_rows: List[Dict[str, Any]] = parse_func(rows)
        print(f"Parsed {len(parsed_rows)} rows")

        for r in parsed_rows:
            yield r

    return wrapper


class BrowserOptionUnsupportedError(Exception):
    pass


@contextmanager
def create_browser_driver(browser_name: str, headless: bool) -> BrowserDriver:
    """
    Context manager creating a Selenium WebDriver based on the given browser name,
    exits if the browser is not supported.
    Accepted browsers are: Chrome, Safari, Firefox, Edge.
    Browser is automatically quit when leaving context manager.

    :param browser_name: name of the browser to create the WebDriver for, should be one of "chrome", "safari", "firefox", "edge", or "ie"
    :param headless: whether to run the browser in headless mode or not
    :return: the created WebDriver
    """

    ua = UserAgent()

    browser_name = browser_name.lower().strip()

    try:
        if browser_name == CHROME:
            options = ChromeOptions()
            user_agent = ua.chrome
            options.add_argument(
                f"--user-agent={user_agent}"
            )

            # TODO -> Check potential non-essential performance-impacting options and disable them
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-in-process-stack-traces")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-crash-reporter")
            options.add_argument("--log-level=3")
            options.add_argument("--output=/dev/null")
            if headless:
                options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        elif browser_name == SAFARI:
            if headless:
                raise BrowserOptionUnsupportedError("As of May 2023, Safari does not support headless mode, "
                                                    "see https://github.com/SeleniumHQ/selenium/issues/12046")
            options = webdriver.SafariOptions()
            user_agent = ua.safari
            options.add_argument(f"--user-agent={user_agent}")
            driver = webdriver.Safari()
        elif browser_name == FIREFOX:
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            user_agent = ua.firefox
            options.add_argument(f"--user-agent={user_agent}")
            driver = webdriver.Firefox(options=options)
        elif browser_name == EDGE:
            options = webdriver.EdgeOptions()
            if headless:
                options.headless = True
            user_agent = ua.edge
            options.add_argument(f"--user-agent={user_agent}")
            driver = webdriver.Edge(options=options)
        else:
            print(f"Unsupported browser: {browser_name}")
            driver = None
            sys.exit(1)
        print(f"Creating {browser_name.capitalize()} browser with User Agent: {user_agent}")
        yield driver
    finally:
        if driver:
            print("Closing browser ...")
            driver.quit()


class ResultsTableNotFoundError(Exception):
    pass


class PageCheckFailedError(Exception):
    pass
