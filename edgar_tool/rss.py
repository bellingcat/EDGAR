import json
import uuid
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

import requests
import xmltodict
from requests import Response

from edgar_tool.constants import RSS_FEED_CSV_FIELDS_NAMES
from edgar_tool.io import write_results_to_file
from edgar_tool.utils import safe_get, unpack_singleton_list

RSS_FEED_DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"
RSS_FEED_URL = "https://www.sec.gov/Archives/edgar/xbrlrss.all.xml"
RSS_COMPANY_TICKERS_FILE_PATH = RSS_FEED_DATA_DIRECTORY / "company_tickers.json"
RSS_COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
UNKNOWN_TICKER_PLACEHOLDER = "UNKNOWN"


def _fetch_company_tickers(
    request_headers: Dict[str, Any], refresh_tickers_mapping: bool
) -> None:
    """
    Fetch the company tickers file from SEC website and save it to the data directory

    :param request_headers: headers to use for the request
    :param refresh_tickers_mapping: whether to refresh the tickers mapping file or not
    """

    # If tickers file is not present or refresh is requested, download the tickers file
    if not RSS_COMPANY_TICKERS_FILE_PATH.exists() or refresh_tickers_mapping:
        print(f"Downloading tickers file at {RSS_COMPANY_TICKERS_URL} ...")
        response = requests.get(RSS_COMPANY_TICKERS_URL, headers=request_headers)
        response.raise_for_status()
        mapping = response.json()
        cik_to_company_mapping = {}
        # Transform the tickers file data to {CIK: [tickers]} format
        print("Transforming tickers file to make it more easily usable ...")
        for _, company_data in mapping.items():
            if cik_to_company_mapping.get(company_data["cik_str"]) is None:
                cik_to_company_mapping[company_data["cik_str"]] = [
                    company_data["ticker"]
                ]
            else:
                cik_to_company_mapping[company_data["cik_str"]].append(
                    company_data["ticker"]
                )
        with open(RSS_COMPANY_TICKERS_FILE_PATH, "wb") as file:
            file.write(
                json.dumps(cik_to_company_mapping, indent=4, sort_keys=True).encode(
                    "utf-8"
                )
            )
        print(f"Successfully saved tickers file to {RSS_COMPANY_TICKERS_FILE_PATH}.")
    else:
        print(
            "Company tickers file found and no refresh requested, skipping download ..."
        )


def resolve_item_cik_and_ticker(
    item: Dict[str, Any], tickers_mapping: Dict[str, List[str]]
) -> Tuple[str, str, List[str]]:
    """
    Resolve the CIK and ticker for a given item in the RSS feed

    :param item: item to resolve the CIK and ticker for
    :param tickers_mapping: mapping of CIK numbers to company tickers
    :return: Tuple of CIK, trimmed CIK, and matching tickers for the item
    """

    # Fetch the CIK number for current item
    cik = safe_get(item, "edgar:xbrlFiling", "edgar:cikNumber")

    # Removing leading zeros from CIK because it's not present in the SEC company tickers file,
    # while it is present in the RSS feed data
    trimmed_cik = cik.lstrip("0") if isinstance(cik, str) else None

    # Try fetching the ticker from the tickers mapping using trimmed CIK
    matching_tickers_for_item_cik: List[str] = tickers_mapping.get(trimmed_cik, [])

    return cik, trimmed_cik, matching_tickers_for_item_cik


def resolve_item_fields(
    item: Dict[str, Any], cik: str, trimmed_cik: str, ticker: str
) -> Dict[str, Any]:
    """
    Resolve the fields for a given item in the RSS feed

    :param item: item to resolve the fields for
    :param cik: CIK number for the current item
    :param trimmed_cik: Trimmed CIK number for the current item
    :param ticker: Ticker for the current item

    :return: Item with resolved fields
    """

    # If current item is not skipped, parse it and yield the parsed data
    parsed_line = {
        "company_name": safe_get(item, "edgar:xbrlFiling", "edgar:companyName"),
        "cik": cik,
        "trimmed_cik": trimmed_cik,
        "ticker": ticker,
        "published_date": item.get("pubDate"),
        "title": item.get("title"),
        "link": item.get("link"),
        "description": item.get("description"),
        "form": safe_get(item, "edgar:xbrlFiling", "edgar:formType"),
        "filing_date": safe_get(item, "edgar:xbrlFiling", "edgar:filingDate"),
        "file_number": safe_get(item, "edgar:xbrlFiling", "edgar:fileNumber"),
        "accession_number": safe_get(item, "edgar:xbrlFiling", "edgar:accessionNumber"),
        "acceptance_date": safe_get(
            item, "edgar:xbrlFiling", "edgar:acceptanceDatetime"
        ),
        "period": safe_get(item, "edgar:xbrlFiling", "edgar:period"),
        "assistant_director": safe_get(
            item, "edgar:xbrlFiling", "edgar:assistantDirector"
        ),
        "assigned_sic": safe_get(item, "edgar:xbrlFiling", "edgar:assignedSic"),
        "fiscal_year_end": safe_get(item, "edgar:xbrlFiling", "edgar:fiscalYearEnd"),
    }

    # Process files URLs
    files_urls = safe_get(item, "edgar:xbrlFiling", "edgar:xbrlFiles", "edgar:xbrlFile")

    files_urls = unpack_singleton_list([f.get("@edgar:url") for f in files_urls])
    parsed_line["xbrl_files"] = files_urls

    return parsed_line


def parse_rss_feed_data(
    response: Response,
    tickers: List[str],
    tickers_mapping: Dict[str, List[str]],
) -> Iterator[Dict[str, Any]]:
    """
    Parse the RSS feed data and yield the parsed data for each item

    :param response: response object containing the RSS feed data
    :param tickers: list of tickers to filter the parsed data with
    :param tickers_mapping: mapping of CIK numbers to company tickers
    This results in the loss of part of the file information, but is more convenient e.g. for CSV format.

    :return: Iterator of parsed dicts for each item in the RSS feed
    """

    # Parse RSS feed data and get all items
    items = xmltodict.parse(response.content)["rss"]["channel"]["item"]
    for i in items:

        try:

            # Resolve the CIK and ticker for the current item
            cik, trimmed_cik, matching_tickers_for_item_cik = (
                resolve_item_cik_and_ticker(i, tickers_mapping)
            )

            # If tickers are provided by user, skip the current item if it doesn't match any of the specified tickers
            if tickers and not any(
                x for x in matching_tickers_for_item_cik if x in tickers
            ):
                continue

            # If tickers are provided by user, try extracting the matched ticker from the tickers mapping
            # If no matched ticker is found or no tickers are provided by user, concatenate the matching tickers
            # for the current CIK into a single string, if no matching tickers are found, use UNKNOWN as placeholder
            matched_ticker_str = (
                next((x for x in matching_tickers_for_item_cik if x in tickers), None)
                or "/".join(matching_tickers_for_item_cik)
                or UNKNOWN_TICKER_PLACEHOLDER
            )

            # Parse the current item
            parsed_item = resolve_item_fields(i, cik, trimmed_cik, matched_ticker_str)

            yield parsed_item

        except Exception as e:
            print(
                f"{e.__class__} occurred while parsing RSS feed item, skipping it: {e.args}"
            )


def fetch_rss_feed(
    tickers: List[str],
    output_file: str,
    refresh_tickers_mapping: bool,
) -> None:
    """
    Fetch the latest RSS feed data for the given company tickers and save it to either a CSV, JSON, or JSONLines file.

    :param tickers: list of company tickers to filter the RSS feed for
    :param output_file: name of the output file to save the results to
    :param refresh_tickers_mapping: whether to refresh the tickers mapping file or not
    """

    # Create the data directory if it doesn't exist
    RSS_FEED_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    # Uppercase and print the tickers to be fetched
    tickers = [x.upper() for x in tickers]
    print(f"Fetching RSS feed for tickers: {', '.join(tickers)}")

    # Create a User-Agent header
    headers = {
        "User-Agent": f"BellingcatEDGARTool_{uuid.uuid4()} contact-tech@bellingcat.com"
    }

    # Fetch the company tickers file if needed/requested
    _fetch_company_tickers(headers, refresh_tickers_mapping)

    # Load the JSON file for CIK numbers
    with open(RSS_COMPANY_TICKERS_FILE_PATH) as file:
        cik_to_ticker_mapping = json.load(file)

    # Fetch the RSS feed
    print(f"Fetching RSS feed from {RSS_FEED_URL}...")
    response = requests.get(RSS_FEED_URL, headers=headers)
    response.raise_for_status()

    # Parse the RSS feed data
    print("Parsing RSS feed XML data...")
    parsed_feed: Iterator[Dict[str, Any]] = parse_rss_feed_data(
        response,
        tickers,
        cik_to_ticker_mapping,
    )

    # Store the parsed data (simulating a generator to reuse the write_results_to_file function used in text search)
    print(f"Saving RSS feed data to {output_file}...")
    write_results_to_file(
        (parsed_feed for _ in range(1)), output_file, RSS_FEED_CSV_FIELDS_NAMES
    )
