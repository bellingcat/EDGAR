from datetime import date, timedelta, datetime
from typing import List, Optional

from src.browser import create_browser_driver, ACCEPTED_BROWSERS
from src.constants import SUPPORTED_OUTPUT_EXTENSIONS, TEXT_SEARCH_FILING_CATEGORIES_MAPPING
from src.rss import daily_rss_feed
from src.text_search import EdgarTextSearcher


def _validate_args(
        search_keywords: List[str],
        start_date: date,
        end_date: date,
        filing_type: Optional[str],
        min_wait_secs: float,
        max_wait_secs: float,
        stop_after_n: int,
        browser_name: str,
        destination: str,
) -> None:
    """
    Validate the CLI arguments, raises an error if the arguments are invalid.
    """

    if not search_keywords:
        raise ValueError("At least one search keyword is required")
    if start_date > end_date:
        raise ValueError("start_date cannot be after end_date")
    if min_wait_secs <= 0:
        raise ValueError("wait_for_request_secs cannot be negative or null")
    if max_wait_secs < min_wait_secs:
        raise ValueError("max_wait_secs cannot be less than min_wait_secs")
    if stop_after_n < 0:
        raise ValueError("stop_after_n cannot be negative")
    if browser_name.lower() not in ACCEPTED_BROWSERS:
        raise ValueError(f"Browser name must be one of: {', '.join(ACCEPTED_BROWSERS)}")
    if not any(destination.lower().endswith(ext) for ext in SUPPORTED_OUTPUT_EXTENSIONS):
        raise ValueError(f"Destination file must have one of the following extensions: {', '.join(SUPPORTED_OUTPUT_EXTENSIONS)}")
    if filing_type and filing_type.lower() not in TEXT_SEARCH_FILING_CATEGORIES_MAPPING.keys():
        raise ValueError(f"Filing type must be one of: {', '.join(TEXT_SEARCH_FILING_CATEGORIES_MAPPING.keys())}")


class SecEdgarScraperCli:

    @staticmethod
    def text_search(
            *keywords: str,
            output: str,
            entity_id: Optional[str] = None,
            filing_type: Optional[str] = None,
            exact_search: bool = False,
            start_date: str = (date.today() - timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
            end_date: str = date.today().strftime("%Y-%m-%d"),
            min_wait: float = 5.0,
            max_wait: float = 8.0,
            retries: int = 3,
            browser: str = "chrome",
            headless: bool = True,
    ) -> None:

        """
        Perform a custom text search on the SEC EDGAR website and save the results to either a CSV or JSONLines file.

        :param keywords: list of keywords to search for
        :param output: Name of the output file to save the results to (CSV or JSONLines format)
        :param entity_id: CIK or name or ticker of the company to search for
        :param filing_type: type of filing to search for
        :param exact_search: whether to perform an exact search or not
        :param start_date: start date of the search
        :param end_date: end date of the search
        :param min_wait: minimum wait time for the request to complete before checking the page or retrying a request
        :param max_wait: maximum wait time for the request to complete before checking the page or retrying a request
        :param retries: how many times to retry requests before failing
        :param browser: name of the browser to use for the search
        :param headless: whether to run the browser in headless mode or not
        """
        try:
            keywords = list(keywords)
            exact_search = bool(exact_search)
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            min_wait = float(min_wait)
            max_wait = float(max_wait)
            retries = int(retries)
            headless = bool(headless)
        except Exception as e:
            raise ValueError(f"Invalid argument type or format: {e}")
        _validate_args(
            search_keywords=keywords,
            start_date=start_date,
            end_date=end_date,
            filing_type=filing_type,
            min_wait_secs=min_wait,
            max_wait_secs=max_wait,
            stop_after_n=retries,
            browser_name=browser,
            destination=output,
        )
        with create_browser_driver(browser, headless=headless) as driver:
            scraper = EdgarTextSearcher(driver=driver)
            scraper.text_search(
                keywords=keywords,
                entity_id=entity_id,
                filing_type=filing_type,
                exact_search=exact_search,
                start_date=start_date,
                end_date=end_date,
                min_wait_seconds=min_wait,
                max_wait_seconds=max_wait,
                retries=retries,
                destination=output,
            )

    @staticmethod
    def rss(*tickers: str, output: str) -> None:
        daily_rss_feed(list(tickers), output)
