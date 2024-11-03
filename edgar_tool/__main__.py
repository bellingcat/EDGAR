from datetime import date, datetime

import typer
from dateutil.relativedelta import relativedelta
from typing_extensions import Annotated

from edgar_tool import constants

app = typer.Typer()


@app.command()
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
    filing_form: Annotated[
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
    # # todo: deprecate min_wait and max_wait
    # min_wait: float = 0.1,
    # max_wait: float = 0.15,
    # retries: int = 3,
    # browser: Optional[str] = None,
    # headless: Optional[bool] = None,
    # peo_in: Optional[str] = None,
    # inc_in: Optional[str] = None,
):
    for t in text:
        print(t)


def main():
    typer.run(text_search)


if __name__ == "__main__":
    main()
