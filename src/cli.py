from datetime import date, timedelta, datetime
from typing import List, Optional

from src.browser import create_browser_driver, ACCEPTED_BROWSERS
from src.edgar import SecEdgarScraper


class SecEdgarScraperCli:

    def _validate_args(
            self,
            search_keywords: List[str],
            start_date: date,
            end_date: date,
            wait_for_request_secs: int,
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
        if wait_for_request_secs <= 0:
            raise ValueError("wait_for_request_secs cannot be negative or null")
        if stop_after_n < 0:
            raise ValueError("stop_after_n cannot be negative")
        if browser_name not in ACCEPTED_BROWSERS:
            raise ValueError(f"Browser name must be one of: {', '.join(ACCEPTED_BROWSERS)}")
        if not destination.endswith(".csv"):
            raise ValueError("Destination file must be a CSV file with a .csv extension")

    def text_search(
            self,
            *keywords: str,
            output: str,
            entity_id: Optional[str] = None,
            filing_type: Optional[str] = None,
            exact_search: bool = False,
            start_date: str = (date.today() - timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
            end_date: str = date.today().strftime("%Y-%m-%d"),
            wait_seconds: int = 8,
            retries: int = 3,
            browser: str = "chrome",
            headless: bool = True,
    ) -> None:

        """
        Perform a custom text search on the SEC EDGAR website and save the results to a CSV file.

        :param keywords: list of keywords to search for
        :param output: Name of the output file to save the results to (CSV format)
        :param entity_id: CIK or name or ticker of the company to search for
        :param filing_type: type of filing to search for
        :param exact_search: whether to perform an exact search or not
        :param start_date: start date of the search
        :param end_date: end date of the search
        :param wait_seconds: how long to wait for requests to complete before retrying
        :param retries: how many times to retry requests before failing
        :param browser: name of the browser to use for the search
        :param headless: whether to run the browser in headless mode or not
        """

        keywords = list(keywords)
        exact_search = bool(exact_search)
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        wait_seconds = int(wait_seconds)
        retries = int(retries)
        headless = bool(headless)
        self._validate_args(
            search_keywords=keywords,
            start_date=start_date,
            end_date=end_date,
            wait_for_request_secs=wait_seconds,
            stop_after_n=retries,
            browser_name=browser,
            destination=output,
        )
        with create_browser_driver(browser, headless=headless) as driver:
            scraper = SecEdgarScraper(driver=driver)
            scraper.text_search(
                keywords=keywords,
                entity_id=entity_id,
                filing_type=filing_type,
                exact_search=exact_search,
                start_date=start_date,
                end_date=end_date,
                wait_seconds=wait_seconds,
                retries=retries,
                destination=output,
            )
