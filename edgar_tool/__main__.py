from datetime import date, datetime
from typing import Optional

import typer
from dateutil.relativedelta import relativedelta
from typing_extensions import Annotated

from edgar_tool import constants, text_search

app = typer.Typer()


@app.command(no_args_is_help=True)
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
        typer.Option(help="Company name, ticker, CIK number or individual's name."),
    ] = None,
    filing_category: Annotated[
        constants.FilingCategory,
        typer.Option(help="Form group to search for."),
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
        ),
    ] = 3,
):
    scraper = text_search.EdgarTextSearcher()
    scraper.text_search(
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


def main():
    typer.run(text_search)


if __name__ == "__main__":
    main()
