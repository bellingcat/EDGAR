import re
import uuid
from typing import Any, Dict, Iterator, List

import pydantic
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from edgar_tool.constants import (
    TEXT_SEARCH_CSV_FIELDS_NAMES,
    TEXT_SEARCH_FORM_MAPPING,
    TEXT_SEARCH_LOCATIONS_MAPPING,
)
from edgar_tool.io import write_results_to_file
from edgar_tool.search_params import SearchParams
from edgar_tool.url_generator import generate_search_url_for_kwargs
from edgar_tool.utils import split_date_range_in_half, unpack_singleton_list


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
        TEXT_SEARCH_FORM_MAPPING.get(form, {}).get("title", "") for form in root_forms
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
        TEXT_SEARCH_LOCATIONS_MAPPING.get(inc_loc) for inc_loc in incorporated_locations
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


def _parse_table_rows(search_request_url: pydantic.HttpUrl) -> List[dict]:
    """
    Parses the given list of table rows into a list of dictionaries.
    Handles multiline rows by joining the text with a line break.

    :param search_request_url: URL of the search request to log in case of errors
    :return: List of dictionaries representing the parsed table rows
    """
    json_response = fetch_page(search_request_url)
    rows = json_response.get("hits", {}).get("hits", [])

    parsed_rows = []
    for i, r in enumerate(rows):
        try:
            parsed = _parse_row(r)
            parsed_rows.append(parsed)
        except Exception as e:
            print(
                f"{e.__class__.__name__} error occurred while parsing row {i + 1} for URL {search_request_url}, skipping ..."
            )
            continue
    return parsed_rows


def search(
    search_params: SearchParams,
    output: str = None,
    max_results: int = None,
) -> None:
    """
    Searches the SEC website for filings based on the given parameters.

    :param search_params: Instance of SearchParams containing the search parameters
    :param output: Name of the CSV file to write the results to. In no output is
      provided, then the results are returned as a list of dictionaries.
    :param max_results: Maximum number of results to return.
    """
    to_return = []
    try:
        for search_url in generate_search_urls(search_params):
            page_results = _parse_table_rows(search_url)
            to_return.extend(page_results)
            if max_results and len(to_return) >= max_results:
                break
    except Exception as e:
        print(
            f"Skipping search request due to an unexpected {e.__class__.__name__} for request parameters '{search_url}': {e}"
        )

    if output:
        write_results_to_file(
            to_return,
            output,
            TEXT_SEARCH_CSV_FIELDS_NAMES,
        )
    if max_results:
        return to_return[:max_results]
    return to_return


class PageCheckFailedError(Exception):
    pass


@retry(
    before=wait_fixed(
        0.11
    ),  # The SEC API limits us to max 10 requests per second. Let's be conservative.
    stop=stop_after_attempt(3),
    reraise=True,
)
def fetch_page(url: pydantic.HttpUrl) -> dict:
    """
    Fetches the given URL and retries the request if the page load fails.

    :param url: URL to fetch
    :return: JSON response from the URL
    """

    print(f"Requesting URL: {url}")
    headers = {
        "User-Agent": f"BellingcatEDGARTool_{uuid.uuid4()} contact-tech@bellingcat.com"
    }
    res = requests.get(str(url), headers=headers)
    if res.status_code != 200:
        raise PageCheckFailedError(f"Error for url {url}, with code {res.status_code}")
    return res.json()


MAX_RESULTS_PER_PAGE = 100


def generate_search_urls(search_params: SearchParams) -> Iterator[pydantic.HttpUrl]:
    """
    Generates search URLs for the given search parameters. Each search URL is
    generated to try and return less than 10,000 results, which is the maximum number of
    results that the SEC API allows us to paginate through. If a search query is
    so vague that a single day contains more than 10,000 results, then the yielded URL is not
    guaranteed to provide all results. This is because the SEC API only allows us to paginate
    through 10,000 results at a time, and we cannot search a date range that is smaller than 1 day.

    :param search_params: Instance of SearchParams containing the search parameters
    :yield: Search URLs
    """
    url = generate_search_url_for_kwargs(search_params)
    json_response = fetch_page(url)
    total_records = int(json_response.get("hits", {}).get("total", {}).get("value", 0))
    search_is_for_single_day = (
        search_params.start_date_formatted is not None
        and search_params.end_date_formatted is not None
        and search_params.start_date_formatted == search_params.end_date_formatted
    )
    if search_is_for_single_day or total_records < 10000:
        yield url
        for page, max_records_per_page in enumerate(
            range(
                MAX_RESULTS_PER_PAGE,
                total_records,
                MAX_RESULTS_PER_PAGE,
            ),
            start=2,
        ):
            yield pydantic.HttpUrl(f"{url}&page={page}&from={max_records_per_page}")
    # The SEC returns a maximum of 10,000 results at a time, so if there are more than
    # 10,000 results, we split the date range in half until we have less than 10,000 results
    else:
        for start, end in split_date_range_in_half(
            search_params.start_date_formatted, search_params.end_date_formatted
        ):
            new_search_params = SearchParams(
                keywords=search_params.keywords,
                entity=search_params.entity,
                filing_category=search_params.filing_category,
                single_forms=search_params.single_forms,
                start_date=start,
                end_date=end,
                inc_in=search_params.inc_in,
                peo_in=search_params.peo_in,
            )
            yield from generate_search_urls(new_search_params)
