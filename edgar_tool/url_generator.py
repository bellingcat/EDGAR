import datetime
from typing import Literal, TypedDict
from urllib import parse


class SearchQueryKwargs(TypedDict, total=False):
    keywords: list[str]
    entity: str
    filing_form: str
    single_forms: list[str]
    date_range_select: Literal["all", "10y", "1y", "30d", "custom"]
    start_date: datetime.date
    end_date: datetime.date
    peo_in: str
    inc_in: str


class _ValidSearchParams:
    def __init__(self, **query_args: SearchQueryKwargs):
        keywords = query_args.get("keywords")
        entity = query_args.get("entity")
        if not keywords and not entity:
            raise ValueError(
                "Invalid search arguments. You must provide keywords or an entity."
            )

        date_range_select = query_args.get("date_range_select")
        start_date = query_args.get("start_date")
        end_date = query_args.get("end_date")
        if date_range_select == "custom" and not (start_date and end_date):
            raise ValueError(
                (
                    "Invalid date parameters. "
                    "You must provide both a start and end date if searching a custom date range."
                )
            )
        elif date_range_select and date_range_select not in {"all", "10y", "1y", "30d"}:
            raise ValueError(
                (
                    "Invalid date_range_select. "
                    'Value must be one of "all", "10y", "1y", "30d", or "custom"'
                )
            )

        self._keywords = keywords
        self.entity = entity
        self.filing_form = query_args.get("filing_form")
        self.single_forms = query_args.get("single_forms")
        self.date_range_select = date_range_select
        self.start_date = start_date
        self.end_date = end_date
        self.peo_in = query_args.get("peo_in")
        self.inc_in = query_args.get("inc_in")

    @property
    def keywords(self):
        return self._keywords

    @keywords.getter
    def keywords(self):
        """Returns the keywords to search for, wrapping exact phrases in quotes."""
        return [f'"{phrase}"' if " " in phrase else phrase for phrase in self._keywords]


def generate_search_url_for_kwargs(search_kwargs: SearchQueryKwargs) -> str:
    base_url = "https://www.sec.gov/edgar/search/#/"
    validated_params = _ValidSearchParams(**search_kwargs)
    query_params = {
        "q": validated_params.keywords,
    }
    encoded_params = parse.urlencode(
        query_params, doseq=True, encoding="utf-8", quote_via=parse.quote
    )
    return parse.urljoin(base=base_url, url=encoded_params, allow_fragments=False)
