import time
from datetime import date, datetime
from typing import Optional

import click
import typer
from dateutil.relativedelta import relativedelta
from typing_extensions import Annotated

from .constants import FilingCategory
from .text_search import EdgarTextSearcher

app = typer.Typer(no_args_is_help=True)


@app.command(
    no_args_is_help=True,
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
            help="Name of the output file to save results to.",
            default_factory=f"edgar_search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        ),
    ],
    start_date: Annotated[
        datetime,
        typer.Option(
            default_factory=(date.today() - relativedelta(years=5)).strftime(
                "%Y-%m-%d"
            ),
            formats=["%Y-%m-%d"],
            help="Start date of the search",
        ),
    ],
    end_date: Annotated[
        datetime,
        typer.Option(
            default_factory=date.today().strftime("%Y-%m-%d"),
            formats=["%Y-%m-%d"],
            help="End date of the search",
        ),
    ],
    entity_id: Annotated[
        str,
        typer.Option(
            help="Company name, ticker, CIK number or individual's name.",
        ),
    ] = None,
    filing_category: Annotated[
        FilingCategory,
        typer.Option(
            help="Form group to search for.",
        ),
    ] = None,
    single_form: Annotated[
        list[str],
        typer.Option(
            "--single-form",
            "-sf",
            help='List of single forms to search for (e.g. `-sf 10-K -sf "PRE 14A")',
        ),
    ] = None,
    peo_in: Annotated[
        Optional[str],
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
        ),
    ] = None,
    inc_in: Annotated[
        Optional[str],
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
        ),
    ] = None,
    # todo: deprecate min_wait and max_wait
    min_wait: Annotated[
        float,
        typer.Option(
            "--min-wait",
            help="Minimum number of seconds to wait between search",
        ),
    ] = 0.1,
    max_wait: Annotated[
        float,
        typer.Option(
            "--max-wait", help="Maximum number of seconds to wait between search"
        ),
    ] = 0.15,
    retries: Annotated[
        int,
        typer.Option(
            "--retries",
            "-r",
            help="Number of times to retry the request before failing",
            click_type=click.IntRange(min=0),
        ),
    ] = 3,
):
    text_searcher = EdgarTextSearcher()
    text_searcher.search(
        keywords=text,
        entity_id=entity_id,
        filing_form=filing_category,
        single_forms=single_form,
        start_date=start_date,
        end_date=end_date,
        min_wait_seconds=min_wait,
        max_wait_seconds=max_wait,
        retries=retries,
        destination=output,
        peo_in=peo_in,
        inc_in=inc_in,
    )


@app.command(
    no_args_is_help=True,
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
            rss.fetch_rss_feed(tickers, output, refresh_tickers_mapping)
            print(
                f"Sleeping for {every_n_mins} minute(s) before fetching the RSS feed again ..."
            )
            time.sleep(every_n_mins * 60)
    rss.fetch_rss_feed(tickers, output, refresh_tickers_mapping)
