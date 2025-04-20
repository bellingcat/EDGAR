import time
from datetime import date, datetime
from typing import Optional

import typer
from typing_extensions import Annotated

from .constants import DateRange, Filing, FilingCategory, Location
from .location_autocomplete import LOCATION_CODE_TO_NAME
from .rss import fetch_rss_feed
from .text_search import SearchParams, search

app = typer.Typer(name="edgar", no_args_is_help=True)


def text_search_output_callback(value: str):
    if not value.endswith(("csv", "json", "jsonl")):
        raise typer.BadParameter(
            f"Unsupported file extension for destination file: {value} "
            "(should be one of csv, json, or jsonl)."
        )
    return value


def location_help_callback(incomplete: str):
    """
    Filters the user's location code input to only show those that start with the input.

    Note that due to the way terminals handle tab completion, we cannot provide fuzzy matches.
    The terminal will only show the matches that start with the input, even if this method returns
    fuzzy matches.
    """
    yield from (
        pair for pair in LOCATION_CODE_TO_NAME if pair.code.startswith(incomplete)
    )


@app.command(
    help=(
        "Perform a custom text search on the SEC EDGAR website and save the results "
        "to either a CSV, JSON, or JSONLines file."
    ),
)
def text_search(
    text: Annotated[
        list[str],
        typer.Argument(
            help=(
                "Search filings for a word or a list of words. "
                "A filing must contain all the words to return. "
                "To search for an exact phrase, use double quotes, like "
                '"fiduciary product".'
            ),
        ),
    ],
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="Name of the output file to save results to. Accepts .csv, .json, and .jsonl extensions.",
            default_factory=f"edgar_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            callback=text_search_output_callback,
        ),
    ],
    date_range: Annotated[
        DateRange,
        typer.Option(
            "--date-range",
            help="Date range of the search. Use 'all' to search all records since 2001.",
        ),
    ] = DateRange.five_years,
    start_date: Annotated[
        datetime,
        typer.Option(
            formats=["%Y-%m-%d"],
            help="Start date of the search in YYYY-MM-DD format (i.e. 2024-07-28). ",
        ),
    ] = None,
    end_date: Annotated[
        datetime,
        typer.Option(
            formats=["%Y-%m-%d"],
            help="End date of the search in YYYY-MM-DD format (i.e. 2024-07-28)",
        ),
    ] = date.today().strftime("%Y-%m-%d"),
    entity_id: Annotated[
        str,
        typer.Option(
            help="Company name, ticker, CIK number or individual's name.",
        ),
    ] = None,
    filing_category: Annotated[
        FilingCategory,
        typer.Option(
            help=(
                "Form group to search for. Use 'custom' or do not set if using "
                "--single-form/-sf."
            ),
        ),
    ] = None,
    single_form: Annotated[
        list[Filing],
        typer.Option(
            "--single-form",
            "-sf",
            help='List of single forms to search for (e.g. -sf 10-K -sf "PRE 14A")',
        ),
    ] = None,
    peo_in: Annotated[
        Location,
        typer.Option(
            "--principal-executive-offices-in",
            "-peoi",
            help=(
                "Search for the primary location associated with a filing. "
                "The principal executive office is where the company's top "
                "management operates and conducts key business decisions. "
                "The location could be a US state or territory, a Canadian "
                "province, or a country."
            ),
            autocompletion=location_help_callback,
        ),
    ] = None,
    inc_in: Annotated[
        Location,
        typer.Option(
            "--incorporated-in",
            "-ii",
            help=(
                "Search for the primary location associated with a filing. "
                "Incorporated in refers to the location where the company was "
                "legally formed and registered as a corporation. "
                "The location could be a US state or territory, a Canadian "
                "province, or a country."
            ),
            autocompletion=location_help_callback,
        ),
    ] = None,
):
    if start_date and end_date and start_date > end_date:
        raise typer.BadParameter("Start date cannot be later than end date.")

    search_params = SearchParams(
        keywords=text,
        entity=entity_id,
        filing_category=filing_category,
        single_forms=single_form,
        date_range_select=date_range,
        start_date=start_date,
        end_date=end_date,
        peo_in=peo_in,
        inc_in=inc_in,
    )

    search(
        search_params=search_params,
        output=output,
    )


def rss_output_callback(value: str):
    if not value.endswith("csv"):
        raise typer.BadParameter(
            f"Unsupported file extension for destination file: {value}. "
            "Only CSV files are supported for RSS feed. Please use a file "
            "that ends with .csv (e.g. --output my_rss_feed.csv)."
        )
    return value


@app.command(
    help=(
        "Fetch the latest RSS feed data for the given company tickers and save it to "
        "either a CSV, JSON, or JSONLines file."
    ),
)
def rss(
    tickers: Annotated[
        list[str],
        typer.Argument(
            help="List of company tickers to fetch the RSS feed for",
        ),
    ],
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help="Name of the output file to save the results to",
            callback=rss_output_callback,
        ),
    ] = f"edgar_rss_feed_{datetime.now().strftime('%d%m%Y_%H%M%S')}.csv",
    refresh_tickers_mapping: Annotated[
        bool,
        typer.Option(
            "--refresh-tickers-mapping",
            "-rtm",
            help="Whether to refresh the company tickers mapping file or not",
        ),
    ] = False,
    every_n_mins: Annotated[
        Optional[int],
        typer.Option(
            "--every-n-mins",
            help="If set, fetch the RSS feed every n minutes",
        ),
    ] = None,
) -> None:
    if every_n_mins:
        while True:
            fetch_rss_feed(tickers, output, refresh_tickers_mapping)
            print(
                f"Sleeping for {every_n_mins} minute(s) before fetching the RSS feed again ..."
            )
            time.sleep(every_n_mins * 60)
    fetch_rss_feed(tickers, output, refresh_tickers_mapping)
