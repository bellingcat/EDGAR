import urllib.parse
from datetime import date, timedelta
from math import ceil
from typing import List, Optional, Dict, Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.browser import (
    BrowserDriver,
    fetch_page,
    extract_html_table_rows,
    PageCheckFailedError,
    ResultsTableNotFoundError,
)
from src.utils import try_or_none

BASE_URL = "https://www.sec.gov/edgar/search/#/"

FILING_CATEGORIES_MAPPING = {
    "all_except_section_16": "form-cat0",
    "all_annual_quarterly_and_current_reports": "form-cat1",
    "all_section_16": "form-cat2",
    "beneficial_ownership_reports": "form-cat3",
    "exempt_offerings": "form-cat4",
    "registration_statements": "form-cat5",
    "filing_review_correspondence": "form-cat6",
    "sec_orders_and_notices": "form-cat7",
    "proxy_materials": "form-cat8",
    "tender_offers_and_going_private_tx": "form-cat9",
    "trust_indentures": "form-cat10",
}

RESULTS_TABLE_SELECTOR = "/html/body/div[3]/div[2]/div[2]/table/tbody"


def check_number_of_pages(driver: BrowserDriver) -> int:
    num_results = driver.find_element(By.ID, "show-result-count").text.split(" ")[0]
    num_pages = ceil(int(num_results) / 100)
    print(f"Found {num_results} results, hence {num_pages} pages")
    return num_pages


def parse_table_rows(rows: List[WebElement]) -> List[dict]:
    """
    Parses the given list of table rows into a list of dictionaries.

    :param rows: List of table rows to parse
    :return: List of dictionaries representing the parsed table rows
    """

    parsed_rows = []
    for r in rows:
        file_link_tag = try_or_none(lambda row: row.find_element(By.CLASS_NAME, "file-num").find_element(By.TAG_NAME, "a"))(r)
        filing_type = try_or_none(lambda row: row.find_element(By.CLASS_NAME, "filetype"))(r)
        filing_type_link = filing_type.find_element(By.CLASS_NAME, "preview-file")
        data_adsh = filing_type_link.get_attribute("data-adsh")
        data_file_name = filing_type_link.get_attribute("data-file-name")
        parsed_rows.append(
            {
                "filing_type": filing_type.text,
                "filed_at": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "filed").text)(r),
                "end_date": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "enddate").text)(r),
                "entity_name": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "entity-name").text)(r),
                "company_cik": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "cik").get_attribute("innerText"))(r),
                "business_location": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "biz-location").get_attribute("innerText"))(r),
                "incorporated_location": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "incorporated").get_attribute("innerText"))(r),
                "file_link": try_or_none(lambda row: file_link_tag.get_attribute("href"))(r),
                "file_num": try_or_none(lambda row: file_link_tag.get_attribute("innerText"))(r),
                "film_num": try_or_none(lambda row: row.find_element(By.CLASS_NAME, "film-num").get_attribute("innerText"))(r),
                "data_adsh": data_adsh,
                "data_file_name": data_file_name,
            }
        )
    return parsed_rows


def generate_request_args(
    search_keywords: List[str],
    entity_identifier: Optional[str] = None,
    filing_category: Optional[str] = None,
    exact_search: bool = False,
    start_date: date = date.today() - timedelta(days=365 * 5),
    end_date: date = date.today(),
    page_number: int = 1,
) -> str:
    """
    Generates the request arguments for the SEC website based on the given parameters.

    :param search_keywords: Search keywords to input in the "Document word or phrase" field
    :param entity_identifier: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
    :param filing_category: Filing category to select from the dropdown menu, defaults to None
    :param exact_search: Whether to perform an exact search on the search_keywords argument or not, defaults to False in order to return the maximum amount of search results by default
    :param start_date: Start date for the custom date range, defaults to 5 years ago to replicate the default behavior of the SEC website
    :param end_date: End date for the custom date range, defaults to current date in order to replicate the default behavior of the SEC website
    :param page_number: Page number to request, defaults to 1

    :return: URL-encoded request arguments string to concatenate to the SEC website URL
    """

    search_keywords = " ".join(search_keywords)
    search_keywords = f'"{search_keywords}"' if exact_search else search_keywords
    request_args = {
        "q": urllib.parse.quote(search_keywords),
        "dateRange": "custom",
        "startdt": start_date.strftime("%Y-%m-%d"),
        "enddt": end_date.strftime("%Y-%m-%d"),
        "page": page_number,
    }

    if entity_identifier:
        request_args["entityName"] = entity_identifier

    if filing_category:
        request_args["category"] = FILING_CATEGORIES_MAPPING[filing_category]

    request_args = urllib.parse.urlencode(request_args)

    return request_args


def paginate_results(
    driver: BrowserDriver,
    start_page: int,
    end_page: int,
    search_keywords: List[str],
    entity_identifier: str,
    filing_category: str,
    exact_search: bool,
    start_date: date,
    end_date: date,
    wait_for_request_secs: int,
    stop_after_n: int,
) -> List[Dict[str, Any]]:
    """
    Paginates through results on the SEC website and returns a list of dictionaries representing the parsed table rows.
    Handles errors gracefully by
        1. retrying the request if the page load fails
        2. returning an empty list if the table is not found

    :param driver: Selenium WebDriver
    :param start_page: first page to fetch
    :param end_page: last page to fetch
    :param search_keywords: search keywords to input in the "Document word or phrase" field
    :param entity_identifier: entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
    :param filing_category: filing category to select from the dropdown menu
    :param exact_search: whether to perform an exact search on the search_keywords argument or not
    :param start_date: start date for the custom date range
    :param end_date: end date for the custom date range
    :param wait_for_request_secs: amount of time to wait for the request to complete
    :param stop_after_n: number of times to retry the request before failing

    :return: list of dictionaries representing the parsed table rows
    """

    results = []
    for i in range(start_page, end_page + 1):
        try:
            print(f"Fetching page {i}")
            request_args = generate_request_args(
                search_keywords=search_keywords,
                entity_identifier=entity_identifier,
                filing_category=filing_category,
                exact_search=exact_search,
                start_date=start_date,
                end_date=end_date,
                page_number=i,
            )

            fetch_page(
                driver, f"{BASE_URL}{request_args}", wait_for_request_secs, stop_after_n
            )

            page_results = extract_html_table_rows(
                driver, By.XPATH, RESULTS_TABLE_SELECTOR
            )(parse_table_rows)
            results.extend(page_results)
        except PageCheckFailedError as e:
            print(
                f"Failed to fetch page {i}, skipping..."
            )
            print(f"Error: {e}")
            continue
        except ResultsTableNotFoundError as e:
            print(
                f"Did not find results table for page {i}, skipping..."
            )
            print(f"Error: {e}")
            continue
        except Exception as e:
            print(
                f"Unexpected error occurred while fetching page {i}, skipping..."
            )
            print(f"Error: {e}")
            continue

    return results


def custom_text_search(
    driver: BrowserDriver,
    search_keywords: List[str],
    entity_identifier: Optional[str] = None,
    filing_category: Optional[str] = None,
    exact_search: bool = False,
    start_date: date = date.today() - timedelta(days=365 * 5),
    end_date: date = date.today(),
    wait_for_request_secs: int = 8,
    stop_after_n: int = 3,
) -> List[Dict[str, Any]]:
    """
    Searches the SEC website for filings based on the given parameters, using Selenium for JavaScript support.

    :param driver: Selenium WebDriver
    :param search_keywords: Search keywords to input in the "Document word or phrase" field
    :param entity_identifier: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
    :param filing_category: Filing category to select from the dropdown menu, defaults to None
    :param exact_search: Whether to perform an exact search on the search_keywords argument or not, defaults to False in order to return the maximum amount of search results by default
    :param start_date: Start date for the custom date range, defaults to 5 years ago to replicate the default behavior of the SEC website
    :param end_date: End date for the custom date range, defaults to current date in order to replicate the default behavior of the SEC website
    :param wait_for_request_secs: Number of seconds to wait for the request to complete, defaults to 10
    :param stop_after_n: Number of times to retry the request before failing, defaults to 3
    :return: None
    """

    results = []

    # Fetch first page, verify that the request was successful by checking the result count value on the page
    request_args = generate_request_args(
        search_keywords=search_keywords,
        entity_identifier=entity_identifier,
        filing_category=filing_category,
        exact_search=exact_search,
        start_date=start_date,
        end_date=end_date,
        page_number=1,
    )
    url = f"{BASE_URL}{request_args}"

    # If we cannot fetch the first page, abort
    try:
        fetch_page(driver, url, wait_for_request_secs, stop_after_n)(
            lambda: driver.find_element(By.XPATH, RESULTS_TABLE_SELECTOR).text.strip() != ""
        )
    except PageCheckFailedError:
        print(f"No results found for first page, aborting...")
        print(f"Please verify that the search/wait/retry parameters are correct and try again.")
        print(f"We recommend disabling headless mode for debugging purposes.")
        raise

    # Get number of pages based on the result count
    try:
        num_pages = check_number_of_pages(driver)
    except Exception as e:
        print(f"Failed to get number of pages, aborting...")
        print(f"Error: {e}")
        raise

    # Get the results from the first page
    results.extend(
        extract_html_table_rows(driver, By.XPATH, RESULTS_TABLE_SELECTOR)(
            parse_table_rows
        )
    )

    # Fetch the rest of the pages and return the results
    results.extend(
        paginate_results(
            driver=driver,
            start_page=2,
            end_page=num_pages,
            search_keywords=search_keywords,
            entity_identifier=entity_identifier,
            filing_category=filing_category,
            exact_search=exact_search,
            start_date=start_date,
            end_date=end_date,
            wait_for_request_secs=wait_for_request_secs,
            stop_after_n=stop_after_n,
        )
    )

    return results
