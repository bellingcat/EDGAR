import itertools
import urllib.parse
from datetime import date, timedelta
from math import ceil
from typing import List, Optional, Dict, Any, Iterator

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.browser import (
    BrowserDriver,
    fetch_page,
    extract_html_table_rows,
    PageCheckFailedError,
    ResultsTableNotFoundError,
)
from src.constants import (
    TEXT_SEARCH_BASE_URL,
    TEXT_SEARCH_FILING_CATEGORIES_MAPPING,
    TEXT_SEARCH_RESULTS_TABLE_XPATH,
    TEXT_SEARCH_SPLIT_BATCHES_NUMBER,
    TEXT_SEARCH_CSV_FIELDS_NAMES,
)
from src.utils import safe_func, split_date_range_in_n
from src.io import write_results_to_file


class EdgarTextSearcher:

    def __init__(self, driver: BrowserDriver):
        self.search_requests = []
        self.driver = driver

    def _parse_number_of_results(self) -> int:

        """
        Parses the number of results found from the search results page.
        :return: Number of results found
        """

        num_results = int(
            self.driver.find_element(By.ID, "show-result-count")
            .text.replace(",", "")
            .split(" ")[0]
        )
        return num_results

    def _compute_number_of_pages(self) -> int:

        """
        Computes the number of pages to paginate through based on the number of results found.

        :return: Number of pages to paginate through
        """

        num_results = self._parse_number_of_results()
        num_pages = ceil(num_results / 100)
        print(f"Found {num_results} / 100 = {num_pages} pages")
        return num_pages

    @staticmethod
    def _parse_table_rows(rows: List[WebElement]) -> List[dict]:
        """
        Parses the given list of table rows into a list of dictionaries.

        :param rows: List of table rows to parse
        :return: List of dictionaries representing the parsed table rows
        """

        parsed_rows = []
        for r in rows:
            file_link_tag = safe_func(
                lambda row: row.find_element(By.CLASS_NAME, "file-num").find_element(
                    By.TAG_NAME, "a"
                )
            )(r)
            filing_type = safe_func(
                lambda row: row.find_element(By.CLASS_NAME, "filetype")
            )(r)
            filing_type_link = safe_func(
                lambda: filing_type.find_element(By.CLASS_NAME, "preview-file")
            )()
            cik = safe_func(
                lambda row: row.find_element(By.CLASS_NAME, "cik")
                .get_attribute("innerText")
                .split(" ")[1]
            )(r)
            cik_cleaned = safe_func(lambda: cik.strip("0"))()
            data_adsh = safe_func(lambda: filing_type_link.get_attribute("data-adsh"))()
            data_adsh_no_dash = safe_func(lambda: data_adsh.replace("-", ""))()
            data_file_name = safe_func(
                lambda: filing_type_link.get_attribute("data-file-name")
            )()
            filing_details_url = f"https://www.sec.gov/Archives/edgar/data/{cik_cleaned}/{data_adsh_no_dash}/{data_adsh}-index.html"
            filing_doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik_cleaned}/{data_adsh_no_dash}/{data_file_name}"
            parsed_rows.append(
                {
                    "filing_type": safe_func(lambda: filing_type.text)(),
                    "filed_at": safe_func(
                        lambda row: row.find_element(By.CLASS_NAME, "filed").text
                    )(r),
                    "reporting_for": safe_func(
                        lambda row: row.find_element(By.CLASS_NAME, "enddate").text
                    )(r),
                    "entity_name": safe_func(
                        lambda row: row.find_element(By.CLASS_NAME, "entity-name").text
                    )(r),
                    "company_cik": cik,
                    "place_of_business": safe_func(
                        lambda row: row.find_element(
                            By.CLASS_NAME, "biz-location"
                        ).get_attribute("innerText")
                    )(r),
                    "incorporated_location": safe_func(
                        lambda row: row.find_element(
                            By.CLASS_NAME, "incorporated"
                        ).get_attribute("innerText")
                    )(r),
                    "file_num": safe_func(
                        lambda row: file_link_tag.get_attribute("innerText")
                    )(r),
                    "film_num": safe_func(
                        lambda row: row.find_element(
                            By.CLASS_NAME, "film-num"
                        ).get_attribute("innerText")
                    )(r),
                    "file_num_search_url": safe_func(
                        lambda row: file_link_tag.get_attribute("href")
                    )(r),
                    "filing_details_url": (
                        filing_details_url
                        if (cik_cleaned and data_adsh_no_dash and data_adsh)
                        else None
                    ),
                    "filing_document_url": (
                        filing_doc_url
                        if (cik_cleaned and data_adsh_no_dash and data_file_name)
                        else None
                    ),
                }
            )
        return parsed_rows

    @staticmethod
    def _generate_request_args(
        keywords: List[str],
        entity_id: Optional[str],
        filing_type: Optional[str],
        exact_search: bool,
        start_date: date,
        end_date: date,
        page_number: int,
    ) -> str:
        """
        Generates the request arguments for the SEC website based on the given parameters.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_type: Filing category to select from the dropdown menu, defaults to None
        :param exact_search: Whether to perform an exact search on the search_keywords argument or not, defaults to False in order to return the maximum amount of search results by default
        :param start_date: Start date for the custom date range, defaults to 5 years ago to replicate the default behavior of the SEC website
        :param end_date: End date for the custom date range, defaults to current date in order to replicate the default behavior of the SEC website
        :param page_number: Page number to request, defaults to 1

        :return: URL-encoded request arguments string to concatenate to the SEC website URL
        """

        # Check that start_date is not after end_date
        if start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        # Join search keywords into a single string
        keywords = " ".join(keywords)
        keywords = f'"{keywords}"' if exact_search else keywords

        # Generate request arguments
        request_args = {
            "q": urllib.parse.quote(keywords),
            "dateRange": "custom",
            "startdt": start_date.strftime("%Y-%m-%d"),
            "enddt": end_date.strftime("%Y-%m-%d"),
            "page": page_number,
        }

        # Add optional parameters
        if entity_id:
            request_args["entityName"] = entity_id
        if filing_type:
            request_args["category"] = TEXT_SEARCH_FILING_CATEGORIES_MAPPING[
                filing_type
            ]

        # URL-encode the request arguments
        request_args = urllib.parse.urlencode(request_args)

        return request_args

    def _fetch_search_request_results(
        self,
        search_request_url_args: str,
        min_wait_seconds: float,
        max_wait_seconds: float,
        retries: int,
    ) -> Iterator[Iterator[Dict[str, Any]]]:
        """
        Fetches the results for the given search request and paginates through the results.

        :param search_request_url_args: URL-encoded request arguments string to concatenate to the SEC website URL
        :param min_wait_seconds: minimum number of seconds to wait for the request to complete
        :param max_wait_seconds: maximum number of seconds to wait for the request to complete
        :param retries: number of times to retry the request before failing
        :return: Iterator of dictionaries representing the parsed table rows
        """

        # Fetch first page, verify that the request was successful by checking the results table appears on the page
        fetch_page(
            self.driver,
            f"{TEXT_SEARCH_BASE_URL}{search_request_url_args}",
            min_wait_seconds,
            max_wait_seconds,
            retries,
        )(
            lambda: self.driver.find_element(
                By.XPATH, TEXT_SEARCH_RESULTS_TABLE_XPATH
            ).text.strip()
            != ""
        )

        # Get number of pages
        num_pages = self._compute_number_of_pages()

        for i in range(1, num_pages + 1):
            paginated_url = f"{TEXT_SEARCH_BASE_URL}{search_request_url_args}&page={i}"
            try:
                fetch_page(
                    self.driver,
                    paginated_url,
                    min_wait_seconds,
                    max_wait_seconds,
                    retries,
                )(
                    lambda: self.driver.find_element(
                        By.XPATH, TEXT_SEARCH_RESULTS_TABLE_XPATH
                    ).text.strip()
                    != ""
                )

                page_results = extract_html_table_rows(
                    self.driver, By.XPATH, TEXT_SEARCH_RESULTS_TABLE_XPATH
                )(self._parse_table_rows)
                yield page_results
            except PageCheckFailedError as e:
                print(f"Failed to fetch page at URL {paginated_url}, skipping...")
                print(f"Error: {e}")
                continue
            except ResultsTableNotFoundError as e:
                print(f"Did not find results table at URL {paginated_url}, skipping...")
                print(f"Error: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error occurred while fetching page {i}, skipping...")
                print(f"Error: {e}")
                continue

    def _generate_search_requests(
        self,
        keywords: List[str],
        entity_id: Optional[str],
        filing_type: Optional[str],
        exact_search: bool,
        start_date: date,
        end_date: date,
        min_wait_seconds: float,
        max_wait_seconds: float,
        retries: int,
    ) -> None:
        """
        Generates search requests for the given parameters and date range,
        recursively splitting the date range in two if the number of results is 10000 or more.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_type: Filing category to select from the dropdown menu
        :param exact_search: Whether to perform an exact search on the search_keywords argument or not
        :param start_date: Start date for the custom date range
        :param end_date: End date for the custom date range
        :param min_wait_seconds: Minimum number of seconds to wait for the request to complete
        :param max_wait_seconds: Maximum number of seconds to wait for the request to complete
        :param retries: Number of times to retry the request before failing
        """

        # Fetch first page, verify that the request was successful by checking the result count value on the page
        request_args = self._generate_request_args(
            keywords=keywords,
            entity_id=entity_id,
            filing_type=filing_type,
            exact_search=exact_search,
            start_date=start_date,
            end_date=end_date,
            page_number=1,
        )
        url = f"{TEXT_SEARCH_BASE_URL}{request_args}"

        # Try to fetch the first page and parse the number of results
        # In rare cases when the results are not empty, but the number of results cannot be parsed,
        # set num_results to 10000 in order to split the date range in two and continue
        try:
            num_results = self._fetch_first_page_results_number(
                url, min_wait_seconds, max_wait_seconds, retries
            )
        except ValueError as ve:
            print(
                f"Setting search results for range {start_date} -> {end_date} to 10000 due to error "
                f"while parsing result number for seemingly non-empty results: {ve}"
            )
            num_results = 10000

        # If we have 10000 results, split date range in two separate requests and fetch first page again, do so until
        # we have a set of date ranges for which none of the requests have 10000 results
        if num_results < 10000:
            print(
                f"Less than 10000 ({num_results}) results found for range {start_date} -> {end_date}, "
                f"returning search request string..."
            )
            self.search_requests.append(request_args)
        else:
            num_batches = min(
                ((end_date - start_date).days, TEXT_SEARCH_SPLIT_BATCHES_NUMBER)
            )
            print(
                f"10000 results or more for date range {start_date} -> {end_date}, splitting in {num_batches} intervals"
            )
            dates = list(split_date_range_in_n(start_date, end_date, num_batches))
            for i, d in enumerate(dates):
                try:
                    start = d if i == 0 else d + timedelta(days=1)
                    end = dates[i + 1]
                    print(
                        f"Trying to generate search requests for date range {start} -> {end} ..."
                    )
                    self._generate_search_requests(
                        keywords=keywords,
                        entity_id=entity_id,
                        filing_type=filing_type,
                        exact_search=exact_search,
                        start_date=start,
                        end_date=end,
                        min_wait_seconds=min_wait_seconds,
                        max_wait_seconds=max_wait_seconds,
                        retries=retries,
                    )
                except IndexError:
                    pass

    def text_search(
        self,
        keywords: List[str],
        entity_id: Optional[str],
        filing_type: Optional[str],
        exact_search: bool,
        start_date: date,
        end_date: date,
        min_wait_seconds: float,
        max_wait_seconds: float,
        retries: int,
        destination: str,
    ) -> None:
        """
        Searches the SEC website for filings based on the given parameters, using Selenium for JavaScript support.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_type: Filing category to select from the dropdown menu
        :param exact_search: Whether to perform an exact search on the search_keywords argument or not
        :param start_date: Start date for the custom date range
        :param end_date: End date for the custom date range
        :param min_wait_seconds: Minimum number of seconds to wait for the request to complete
        :param max_wait_seconds: Maximum number of seconds to wait for the request to complete
        :param retries: Number of times to retry the request before failing
        :param destination: Name of the CSV file to write the results to
        """

        self._generate_search_requests(
            keywords=keywords,
            entity_id=entity_id,
            filing_type=filing_type,
            exact_search=exact_search,
            start_date=start_date,
            end_date=end_date,
            min_wait_seconds=min_wait_seconds,
            max_wait_seconds=max_wait_seconds,
            retries=retries,
        )

        search_requests_results: List[Iterator[Iterator[Dict[str, Any]]]] = []
        for r in self.search_requests:

            # Run generated search requests and paginate through results
            try:
                all_pages_results: Iterator[Iterator[Dict[str, Any]]] = (
                    self._fetch_search_request_results(
                        search_request_url_args=r,
                        min_wait_seconds=min_wait_seconds,
                        max_wait_seconds=max_wait_seconds,
                        retries=retries,
                    )
                )
                search_requests_results.append(all_pages_results)

            except Exception as e:
                print(
                    f"Unexpected error occurred while fetching search request results for request parameters '{r}': {e}"
                )
                print(f"Skipping...")

        write_results_to_file(
            itertools.chain(*search_requests_results),
            destination,
            TEXT_SEARCH_CSV_FIELDS_NAMES,
        )

    def _fetch_first_page_results_number(
        self, url: str, min_wait_seconds: float, max_wait_seconds: float, retries: int
    ) -> int:
        """
        Fetches the first page of results for the given URL and returns the number of results.

        :param url: URL to fetch the first page of results from
        :param min_wait_seconds: Minimum number of seconds to wait for the request to complete
        :param max_wait_seconds: Maximum number of seconds to wait for the request to complete
        :param retries: Number of times to retry the request before failing
        :return: Number of results found for the given URL
        """

        # If we cannot fetch the first page after retries, abort
        try:
            fetch_page(self.driver, url, min_wait_seconds, max_wait_seconds, retries)(
                lambda: self.driver.find_element(
                    By.XPATH, TEXT_SEARCH_RESULTS_TABLE_XPATH
                ).text.strip()
                != ""
            )
        except PageCheckFailedError as e:
            print(f"First page check at URL failed due to {e.__class__.__name__}: \n{e}")
            print(f"No results found for first page at URL {url}, aborting...")
            print(f"Please verify that the search/wait/retry parameters are correct and try again.")
            print(f"We recommend disabling headless mode for debugging purposes.")
            raise

        # If we cannot get number of results after retries, abort
        try:
            num_results = self._parse_number_of_results()
            return num_results
        except Exception as e:
            print(f"Failed to parse number of results for URL {url}, aborting...")
            print(f"Error: {e}")
            raise
