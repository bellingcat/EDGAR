import itertools
import sys
import urllib.parse
from datetime import date, timedelta
from math import ceil
from typing import List, Optional, Dict, Any, Iterator

from bs4 import BeautifulSoup
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
from src.io import write_results_to_file
from src.utils import split_date_range_in_n, unpack_singleton_list


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
    def split_html_by_line(element: WebElement) -> List[str]:
        """
        Handles line breaks in the given WebElement's innerHTML attribute.
        This fixes an issue due to innerText trimming line breaks.

        :param element: WebElement to handle line breaks for
        :return: InnerHTML with line breaks replaced by a space
        """

        return element.get_attribute("innerHTML").split("<br>")

    @staticmethod
    def _parse_row(row: WebElement) -> Dict[str, Any]:
        """
        Parses the given table row into a dictionary.

        :param row: Table row to parse
        :return: Dictionary representing the parsed table row
        """

        # Fetching outerHTML and parsing it with BeautifulSoup
        html = row.get_attribute("outerHTML")
        soup = BeautifulSoup(html, "html.parser").find("tr")

        # Fetching file numbers and links
        file_nums_tags = soup.find("td", class_="file-num").find_all("a", href=True)
        file_nums = [x.text for x in file_nums_tags]
        file_nums_search_urls = [x.get("href") for x in file_nums_tags]

        # Fetching film numbers
        film_nums = [
            x.text
            for x in soup.find("td", class_="film-num")
            if x.text and "<br/>" not in x
        ]

        # Fetching and cleaning CIKs
        ciks = [
            x.text.replace("CIK ", "").strip()
            for x in soup.find("td", class_="cik")
            if "CIK" in x
        ]
        ciks_trimmed: List[str] = [c.strip("0") for c in ciks]

        # Fetching filing type and link
        filing_type = soup.find("td", class_="filetype").find("a", href=True)
        data_file_name = filing_type.get("data-file-name")
        data_adsh = filing_type.get("data-adsh")
        filing_type = filing_type.text.strip()
        data_adsh_no_dash = data_adsh.replace("-", "")

        # Building URLs for filing details and documents
        filing_details_urls: List[str] = [
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{data_adsh_no_dash}/{data_adsh}-index.html"
            for cik in ciks_trimmed
        ]
        filing_details_urls: str = (
            unpack_singleton_list(filing_details_urls)
            if (ciks_trimmed and data_adsh_no_dash and data_adsh)
            else None
        )
        filing_doc_urls: List[str] = [
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{data_adsh_no_dash}/{data_file_name}"
            for cik in ciks_trimmed
        ]
        filing_doc_urls: str = unpack_singleton_list(filing_doc_urls)
        filed_at = soup.find("td", class_="filed").text.strip()
        end_date = soup.find("td", class_="enddate").text.strip()
        entity_names = [
            x.text.strip().replace("\n", "")
            for x in soup.find("td", class_="entity-name")
            if x.text and "<br/>" not in x
        ]
        places_of_business = [
            x.text.strip()
            for x in soup.find("td", class_="biz-location")
            if x.text and "<br/>" not in x
        ]
        incorporated_locations = [
            x.text.strip()
            for x in soup.find("td", class_="incorporated")
            if x.text and "<br/>" not in x
        ]

        parsed = {
            "filing_type": filing_type,
            "filed_at": filed_at,
            "reporting_for": end_date,
            "entity_name": unpack_singleton_list(entity_names),
            "company_cik": unpack_singleton_list(ciks),
            "company_cik_trimmed": unpack_singleton_list(ciks_trimmed),
            "place_of_business": unpack_singleton_list(places_of_business),
            "incorporated_location": unpack_singleton_list(incorporated_locations),
            "file_num": unpack_singleton_list(file_nums),
            "file_num_search_url": unpack_singleton_list(file_nums_search_urls),
            "film_num": unpack_singleton_list(film_nums),
            "filing_details_url": filing_details_urls,
            "filing_document_url": filing_doc_urls,
        }

        return parsed

    def _parse_table_rows(
        self, rows: List[WebElement], search_request_url: str
    ) -> List[dict]:
        """
        Parses the given list of table rows into a list of dictionaries.
        Handles multiline rows by joining the text with a line break.

        :param rows: List of table rows to parse
        :param search_request_url: URL of the search request to log in case of errors
        :return: List of dictionaries representing the parsed table rows
        """

        parsed_rows = []
        for i, r in enumerate(rows):
            try:
                parsed = self._parse_row(r)
                parsed_rows.append(parsed)
            except Exception as e:
                print(
                    f"{e.__class__.__name__} error occurred while parsing row {i + 1} for URL {search_request_url}, skipping ..."
                )
                continue
        return parsed_rows

    @staticmethod
    def _generate_request_args(
        keywords: List[str],
        entity_id: Optional[str],
        filing_type: Optional[str],
        start_date: date,
        end_date: date,
        page_number: int,
    ) -> str:
        """
        Generates the request arguments for the SEC website based on the given parameters.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_type: Filing category to select from the dropdown menu, defaults to None
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
            != "",
            f"First search request failed for URL {TEXT_SEARCH_BASE_URL}{search_request_url_args} ...",
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
                    != "",
                    f"Search request failed for page {i} at URL {paginated_url}, skipping page...",
                )

                page_results = extract_html_table_rows(
                    self.driver, By.XPATH, TEXT_SEARCH_RESULTS_TABLE_XPATH
                )(lambda x: self._parse_table_rows(x, paginated_url))
                yield page_results
            except PageCheckFailedError as e:
                print(e)
                continue
            except ResultsTableNotFoundError:
                print(f"Could not find results table on page {i} at URL {paginated_url}, skipping page...")
                continue
            except Exception as e:
                print(f"Unexpected {e.__class__.__name__} error occurred while fetching page {i} at URL {paginated_url}, skipping page: {e}")
                continue

    def _generate_search_requests(
        self,
        keywords: List[str],
        entity_id: Optional[str],
        filing_type: Optional[str],
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
                    f"Skipping search request due to an unexpected {e.__class__.__name__} for request parameters '{r}': {e}"
                )

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
                != "",
                f"No results found on first page at URL {url}, aborting...\n"
                f"Please verify that the search/wait/retry parameters are correct and try again.\n"
                f"We recommend disabling headless mode for debugging purposes."
            )
        except PageCheckFailedError as e:
            print(e)
            sys.exit(1)

        # If we cannot get number of results after retries, abort
        try:
            num_results = self._parse_number_of_results()
            return num_results
        except Exception as e:
            print(f"Execution aborting due to a {e.__class__.__name__} error raised "
                  f"while parsing number of results for first page at URL {url}: {e}")
            sys.exit(1)
