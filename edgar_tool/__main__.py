from datetime import datetime

import typer
from typing_extensions import Annotated

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
    # entity_id: Optional[str] = None,
    # filing_form: Optional[str] = None,
    # single_forms: Optional[list[str]] = None,
    # start_date: str = (date.today() - timedelta(days=365 * 5)).strftime("%Y-%m-%d"),
    # end_date: str = date.today().strftime("%Y-%m-%d"),
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
