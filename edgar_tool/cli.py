import time
from datetime import date, timedelta, datetime
from typing import List, Optional
from warnings import warn
from edgar_tool.constants import (
    SUPPORTED_OUTPUT_EXTENSIONS,
    TEXT_SEARCH_FILING_CATEGORIES_MAPPING,
)
from edgar_tool.rss import fetch_rss_feed
from edgar_tool.text_search import EdgarTextSearcher


def _validate_text_search_args(
    search_keywords: List[str],
    start_date: date,
    end_date: date,
    filing_type: Optional[str],
    min_wait_secs: float,
    max_wait_secs: float,
    retries: int,
    browser_name: Optional[str],
    headless: Optional[bool],
    destination: str,
) -> None:
    """
    Validate the text search CLI arguments, raises an error if the arguments are invalid.
    """

    if not search_keywords:
        raise ValueError("At least one search keyword is required")
    if start_date > end_date:
        raise ValueError("start_date cannot be after end_date")
    if min_wait_secs < 0.1:
        raise ValueError("wait_for_request_secs cannot be less than 0.1 seconds")
    if max_wait_secs < min_wait_secs:
        raise ValueError("max_wait_secs cannot be less than min_wait_secs")
    if retries < 0:
        raise ValueError("retries cannot be negative")
    if browser_name is not None:
        warn("browser argument is deprecated and is ignored")
    if headless is not None:
        warn("headless argument is deprecated and is ignored")
    if not any(
        destination.lower().endswith(ext) for ext in SUPPORTED_OUTPUT_EXTENSIONS
    ):
        raise ValueError(
            f"Destination file must have one of the following extensions: {', '.join(SUPPORTED_OUTPUT_EXTENSIONS)}"
        )
    if (
        filing_type
        and filing_type.lower() not in TEXT_SEARCH_FILING_CATEGORIES_MAPPING.keys()
    ):
        raise ValueError(
            f"Filing type must be one of: {', '.join(TEXT_SEARCH_FILING_CATEGORIES_MAPPING.keys())}"
        )


class SecEdgarScraperCli:

    @staticmethod
    def text_search(
        *keywords: str,
        output: str = f"edgar_search_results_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv",
        entity_id: Optional[str] = None,
        filing_type: Optional[str] = None,
        start_date: str = (date.today() - timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
        end_date: str = date.today().strftime("%Y-%m-%d"),
        # todo: deprecate min_wait and max_wait
        min_wait: float = 0.1,
        max_wait: float = 0.15,
        retries: int = 3,
        browser: Optional[str] = None,
        headless: Optional[bool] = None,
    ) -> None:
        """
        Perform a custom text search on the SEC EDGAR website and save the results to either a CSV, JSON,
        or JSONLines file.

        :param keywords: List of keywords to search for
        :param output: Name of the output file to save the results to
        :param entity_id: CIK or name or ticker of the company to search for
        :param filing_type: Type of filing to search for
        :param start_date: Start date of the search
        :param end_date: End date of the search
        :param min_wait: Minimum wait time for the request to complete before checking the page or retrying a request
        :param max_wait: Maximum wait time for the request to complete before checking the page or retrying a request
        :param retries: How many times to retry requests before failing
        :param browser: Deprecated and not used
        :param headless: Deprecated and not used
        """
        try:
            keywords = list(keywords)
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            min_wait = float(min_wait)
            max_wait = float(max_wait)
            retries = int(retries)
        except Exception as e:
            raise ValueError(f"Invalid argument type or format: {e}")
        _validate_text_search_args(
            search_keywords=keywords,
            start_date=start_date,
            end_date=end_date,
            filing_type=filing_type,
            min_wait_secs=min_wait,
            max_wait_secs=max_wait,
            retries=retries,
            browser_name=browser,
            headless=headless,
            destination=output,
        )
        scraper = EdgarTextSearcher()
        scraper.text_search(
            keywords=keywords,
            entity_id=entity_id,
            filing_type=filing_type,
            start_date=start_date,
            end_date=end_date,
            min_wait_seconds=min_wait,
            max_wait_seconds=max_wait,
            retries=retries,
            destination=output,
        )

    @staticmethod
    def rss(
        *tickers: str,
        output: str = f"edgar_rss_feed_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv",
        refresh_tickers_mapping: bool = False,
        every_n_mins: Optional[int] = None,
    ) -> None:
        """
        Fetch the latest RSS feed data for the given company tickers and save it to either a CSV, JSON,
        or JSONLines file.
        :param tickers: List of company tickers to fetch the RSS feed for
        :param output: Name of the output file to save the results to
        :param refresh_tickers_mapping: Whether to refresh the company tickers mapping file or not
        :param every_n_mins: If set, fetch the RSS feed every n minutes
        """
        try:
            tickers = list(tickers)
            refresh_tickers_mapping = bool(refresh_tickers_mapping)
            if every_n_mins:
                every_n_mins = int(every_n_mins)
        except Exception as e:
            raise ValueError(f"Invalid argument type or format: {e}")

        if every_n_mins:
            while True:
                fetch_rss_feed(tickers, output, refresh_tickers_mapping)
                print(
                    f"Sleeping for {every_n_mins} minute(s) before fetching the RSS feed again ..."
                )
                time.sleep(every_n_mins * 60)
        else:
            fetch_rss_feed(tickers, output, refresh_tickers_mapping)
