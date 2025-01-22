import itertools
import re
import sys
import urllib.parse
from datetime import date, timedelta
from math import ceil
from typing import Any, Dict, Iterator, List, Optional

from edgar_tool.constants import (
    TEXT_SEARCH_BASE_URL,
    TEXT_SEARCH_CATEGORY_FORM_GROUPINGS,
    TEXT_SEARCH_CSV_FIELDS_NAMES,
    TEXT_SEARCH_FORM_MAPPING,
    TEXT_SEARCH_LOCATIONS_MAPPING,
    TEXT_SEARCH_SPLIT_BATCHES_NUMBER,
)
from edgar_tool.io import write_results_to_file
from edgar_tool.page_fetcher import (
    NoResultsFoundError,
    PageCheckFailedError,
    ResultsTableNotFoundError,
    fetch_page,
)
from edgar_tool.utils import split_date_range_in_n, unpack_singleton_list


class EdgarTextSearcher:

    def __init__(self):
        self.search_requests = []
        self.json_response = {}

    def _parse_number_of_results(self) -> int:
        """
        Parses the number of results found from the search results page.
        :return: Number of results found
        """
        try:
            num_results = int(
                self.json_response.get("hits", {}).get("total", {}).get("value", 0)
            )
            return num_results

        except NoResultsFoundError as e:
            raise NoResultsFoundError("no results to parse") from e

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
    def _parse_row(row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the given table row into a dictionary.

        :param row: Table row to parse
        :return: Dictionary representing the parsed table row
        """
        _id = row.get("_id", "").split(":")[-1]
        _source = row.get("_source", {})

        # Fetching file numbers and links
        file_nums = _source.get("file_num", [])
        file_nums_search_urls = [
            f"https://www.sec.gov/cgi-bin/browse-edgar/?filenum={file_num}&action=getcompany"
            for file_num in file_nums
        ]

        # Fetching film numbers
        film_nums = _source.get("film_num")

        # Fetching and cleaning CIKs
        ciks = _source.get("ciks")
        ciks_trimmed: List[str] = [c.lstrip("0") for c in ciks]

        # Get form and human readable name
        root_forms = _source.get("root_forms")
        form_name = [
            TEXT_SEARCH_FORM_MAPPING.get(form, {}).get("title", "")
            for form in root_forms
        ]
        root_forms = unpack_singleton_list(root_forms)
        form_name = unpack_singleton_list(form_name)

        # Build adsh for url
        data_adsh = _source.get("adsh", "")
        data_adsh_no_dash = data_adsh.replace("-", "")

        # Building URLs for filing details and documents
        filing_details_urls: List[str] = [
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{data_adsh_no_dash}/{data_adsh}-index.html"
            for cik in ciks_trimmed
        ]
        filing_details_urls: str = (
            unpack_singleton_list(filing_details_urls)
            if (ciks_trimmed and data_adsh)
            else None
        )
        filing_doc_urls: List[str] = [
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{data_adsh_no_dash}/{_id}"
            for cik in ciks_trimmed
        ]
        filing_doc_urls: str = unpack_singleton_list(filing_doc_urls)

        filed_at = _source.get("file_date")
        end_date = _source.get("period_ending")
        entity_names = [
            name.replace("\n", "").rsplit("  (CIK ", maxsplit=1)[
                0
            ]  # Remove Newlines and CIK from name
            for name in _source.get("display_names", [])
        ]

        # Extract tickers from entity names
        ticker_regex = r"\(([A-Z\s,\-]+)\)+$"

        tickers = [
            ticker.group(1)
            for name in entity_names
            if (ticker := re.search(ticker_regex, name)) and ticker is not None
        ]
        tickers = tickers if len(tickers) != 0 else None

        # Remove tickers from entity names
        entity_names = [re.sub(ticker_regex, "", name).strip() for name in entity_names]

        places_of_business = _source.get("biz_locations")
        places_of_business = [
            (
                f"{split[0]}, {TEXT_SEARCH_LOCATIONS_MAPPING.get(split[1])}"
                if len(split) == 2
                else f"{split[0]}"
            )
            for place in places_of_business
            if (split := place.rsplit(", ", maxsplit=1))
        ]

        incorporated_locations = _source.get("inc_states")
        incorporated_locations = [
            TEXT_SEARCH_LOCATIONS_MAPPING.get(inc_loc)
            for inc_loc in incorporated_locations
        ]

        parsed = {
            "root_form": root_forms,
            "form_name": form_name,
            "filed_at": filed_at,
            "reporting_for": end_date,
            "entity_name": unpack_singleton_list(entity_names),
            "ticker": unpack_singleton_list(tickers),
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

    def _parse_table_rows(self, search_request_url: str) -> List[dict]:
        """
        Parses the given list of table rows into a list of dictionaries.
        Handles multiline rows by joining the text with a line break.

        :param search_request_url: URL of the search request to log in case of errors
        :return: List of dictionaries representing the parsed table rows
        """
        rows = self.json_response.get("hits", {}).get("hits", [])

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
        filing_form: Optional[str],
        single_forms: Optional[List[str]],
        start_date: date,
        end_date: date,
        peo_in: Optional[str],
        inc_in: Optional[str],
    ) -> str:
        """
        Generates the request arguments for the SEC website based on the given parameters.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_form: Group to select within the filing category dropdown menu, defaults to None
        :param single_forms: List of single forms to search for (e.g. ['10-K', '10-Q']), defaults to None
        :param start_date: Start date for the custom date range, defaults to 5 years ago to replicate the default behavior of the SEC website
        :param end_date: End date for the custom date range, defaults to current date in order to replicate the default behavior of the SEC website
        :param peo_in: Search principal executive offices in a location (e.g. "NY,OH")
        :param inc_in: Search incorporated in a location (e.g. "NY,OH")

        :return: URL-encoded request arguments string to concatenate to the SEC website URL
        """

        # Check that start_date is not after end_date
        if start_date > end_date:
            raise ValueError("start_date cannot be after end_date")

        # Join search keywords into a single string
        keywords = " ".join(
            [f'"{keyword}"' if " " in keyword else keyword for keyword in keywords]
        )

        # Generate request arguments
        request_args = {
            "q": keywords,
            "dateRange": "custom",
            "startdt": start_date.strftime("%Y-%m-%d"),
            "enddt": end_date.strftime("%Y-%m-%d"),
        }

        # Add optional parameters
        if peo_in and inc_in:
            raise ValueError(
                "use only one of peo_in or inc_in, not both"
            )  ## because SEC API doesn't support
        else:
            if peo_in:
                request_args["locationCodes"] = peo_in
            if inc_in:
                request_args["locationCodes"] = inc_in
                request_args["locationType"] = "incorporated"

        if entity_id:
            request_args["entityName"] = entity_id
        # Handle forms and single forms
        part_filing_form = (
            []
            if filing_form is None
            else TEXT_SEARCH_CATEGORY_FORM_GROUPINGS[filing_form]
        )
        part_single_forms = [] if single_forms is None else single_forms

        # Join the filing_forms and single forms and remove duplicates
        forms = ",".join(list(set(part_filing_form + part_single_forms)))
        if forms != "":
            request_args["forms"] = forms

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
        self.json_response = fetch_page(
            f"{TEXT_SEARCH_BASE_URL}{search_request_url_args}",
            min_wait_seconds,
            max_wait_seconds,
            retries,
        )(
            lambda json_response: json_response.get("error") is None
            and json_response.get("hits", {}).get("hits", 0) != 0,
            f"First search request failed for URL {TEXT_SEARCH_BASE_URL}{search_request_url_args} ...",
        )

        # Get number of pages
        num_pages = self._compute_number_of_pages()

        for i in range(1, num_pages + 1):
            paginated_url = f"{TEXT_SEARCH_BASE_URL}{search_request_url_args}&page={i}&from={100*(i-1)}"
            try:
                self.json_response = fetch_page(
                    paginated_url,
                    min_wait_seconds,
                    max_wait_seconds,
                    retries,
                )(
                    lambda json_response: json_response.get("error") is None,
                    f"Search request failed for page {i} at URL {paginated_url}, skipping page...",
                )
                if self.json_response.get("hits", {}).get("hits", 0) == 0:
                    raise ResultsTableNotFoundError()
                page_results = self._parse_table_rows(paginated_url)
                yield page_results
            except PageCheckFailedError as e:
                print(e)
                continue
            except ResultsTableNotFoundError:
                print(
                    f"Could not find results table on page {i} at URL {paginated_url}, skipping page..."
                )
                continue
            except Exception as e:
                print(
                    f"Unexpected {e.__class__.__name__} error occurred while fetching page {i} at URL {paginated_url}, skipping page: {e}"
                )
                continue

    def _generate_search_requests(
        self,
        keywords: List[str],
        entity_id: Optional[str],
        filing_form: Optional[str],
        single_forms: Optional[List[str]],
        start_date: date,
        end_date: date,
        min_wait_seconds: float,
        max_wait_seconds: float,
        retries: int,
        peo_in: Optional[str],
        inc_in: Optional[str],
    ) -> None:
        """
        Generates search requests for the given parameters and date range,
        recursively splitting the date range in two if the number of results is 10000 or more.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_form: Group to select within the filing category dropdown menu, defaults to None
        :param single_forms: List of single forms to search for (e.g. ['10-K', '10-Q']), defaults to None
        :param start_date: Start date for the custom date range
        :param end_date: End date for the custom date range
        :param min_wait_seconds: Minimum number of seconds to wait for the request to complete
        :param max_wait_seconds: Maximum number of seconds to wait for the request to complete
        :param retries: Number of times to retry the request before failing
        :param peo_in: Search principal executive offices in a location (e.g. "NY,OH")
        :param inc_in: Search incorporated in a location (e.g. "NY,OH")
        """

        # Fetch first page, verify that the request was successful by checking the result count value on the page
        request_args = self._generate_request_args(
            keywords=keywords,
            entity_id=entity_id,
            filing_form=filing_form,
            single_forms=single_forms,
            start_date=start_date,
            end_date=end_date,
            peo_in=peo_in,
            inc_in=inc_in,
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
        if num_results == 0:
            print(
                f"No results found for query in date range {start_date} -> {end_date}."
            )
        elif num_results < 10000:
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
                        filing_form=filing_form,
                        single_forms=single_forms,
                        start_date=start,
                        end_date=end,
                        min_wait_seconds=min_wait_seconds,
                        max_wait_seconds=max_wait_seconds,
                        retries=retries,
                        peo_in=peo_in,
                        inc_in=inc_in,
                    )
                except IndexError:
                    pass

    def text_search(
        self,
        keywords: List[str],
        entity_id: Optional[str],
        filing_form: Optional[str],
        single_forms: Optional[List[str]],
        start_date: date,
        end_date: date,
        min_wait_seconds: float,
        max_wait_seconds: float,
        retries: int,
        destination: str,
        peo_in: Optional[str],
        inc_in: Optional[str],
    ) -> None:
        """
        Searches the SEC website for filings based on the given parameters.

        :param keywords: Search keywords to input in the "Document word or phrase" field
        :param entity_id: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
        :param filing_form: Group to select within the filing category dropdown menu, defaults to None
        :param single_forms: List of single forms to search for (e.g. ['10-K', '10-Q']), defaults to None
        :param start_date: Start date for the custom date range
        :param end_date: End date for the custom date range
        :param min_wait_seconds: Minimum number of seconds to wait for the request to complete
        :param max_wait_seconds: Maximum number of seconds to wait for the request to complete
        :param retries: Number of times to retry the request before failing
        :param destination: Name of the CSV file to write the results to
        :param peo_in: Search principal executive offices in a location (e.g. "NY,OH")
        :param inc_in: Search incorporated in a location (e.g. "NY,OH")
        """
        self._generate_search_requests(
            keywords=keywords,
            entity_id=entity_id,
            filing_form=filing_form,
            single_forms=single_forms,
            start_date=start_date,
            end_date=end_date,
            min_wait_seconds=min_wait_seconds,
            max_wait_seconds=max_wait_seconds,
            retries=retries,
            peo_in=peo_in,
            inc_in=inc_in,
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
        if search_requests_results == []:
            raise NoResultsFoundError(f"No results found for the search query")
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
            self.json_response = fetch_page(
                url,
                min_wait_seconds,
                max_wait_seconds,
                retries,
            )(lambda json_response: json_response.get("hits", {}).get("hits", 0) != 0)
        except PageCheckFailedError as e:
            raise PageCheckFailedError(
                f"\n{e}. "
                f"Please verify that the search/wait/retry parameters are correct and try again."
            ) from e

        # If we cannot get number of results after retries, abort
        try:
            num_results = self._parse_number_of_results()
            return num_results
        except NoResultsFoundError as e:
            raise NoResultsFoundError(
                f"\nExecution aborting due to a {e.__class__.__name__} error raised "
                f"while parsing number of results for first page at URL {url}: {e}"
            ) from e
