import datetime
from typing import Literal, TypedDict
from urllib import parse

from edgar_tool.constants import PEO_IN_AND_INC_IN_TO_SEC_FORM_ID


class SearchQueryKwargs(TypedDict, total=False):
    keywords: list[str]
    entity: str
    filing_category: str
    single_forms: list[str]
    date_range_select: Literal["all", "10y", "1y", "30d", "custom"]
    start_date: datetime.date
    end_date: datetime.date
    inc_in: str
    peo_in: str


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
        elif date_range_select and date_range_select not in {
            "all",
            "10y",
            "1y",
            "30d",
            "custom",
        }:
            raise ValueError(
                (
                    "Invalid date_range_select. "
                    'Value must be one of "all", "10y", "1y", "30d", or "custom"'
                )
            )

        self._keywords = keywords
        self.entity = entity

        filing_category = query_args.get("filing_category", "custom")
        single_forms = query_args.get("single_forms")
        if filing_category != "custom" and single_forms:
            raise ValueError(
                "Cannot specify both filing_category and single_forms. "
                "Passing single_forms automatically sets the filing_category"
                " to custom. Please choose one or the other."
            )

        self._filing_category = filing_category
        self.single_forms = single_forms
        self.date_range_select = date_range_select
        self.start_date = start_date
        self.end_date = end_date

        peo_in = query_args.get("peo_in")
        if peo_in and peo_in not in PEO_IN_AND_INC_IN_TO_SEC_FORM_ID:
            raise ValueError(
                (
                    "Invalid location code. "
                    "Please provide a valid 2-letter state abbreviation, "
                    "3-letter country code, or 'XX' for unknown."
                )
            )
        inc_in = query_args.get("inc_in")
        self.inc_in = inc_in
        self.peo_in = peo_in

    @property
    def keywords(self):
        return self._keywords

    @keywords.getter
    def keywords(self):
        """Returns the keywords to search for, wrapping exact phrases in quotes."""
        return [f'"{phrase}"' if " " in phrase else phrase for phrase in self._keywords]

    @property
    def filing_category(self):
        return self._filing_category

    @keywords.getter
    def filing_category(self):
        filing_category_to_sec_form_id = {
            "all": "",
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
        return filing_category_to_sec_form_id.get(self._filing_category)


def generate_search_url_for_kwargs(search_kwargs: SearchQueryKwargs) -> str:
    base_url = "https://www.sec.gov/edgar/search/#/"
    validated_params = _ValidSearchParams(**search_kwargs)
    query_params = {
        "q": validated_params.keywords,
    }
    if date_range_select := validated_params.date_range_select:
        query_params.update(
            {
                "dateRange": date_range_select,
            }
        )
        if date_range_select == "custom":
            query_params.update(
                {
                    "startdt": validated_params.start_date.strftime("%Y-%m-%d"),
                    "enddt": validated_params.end_date.strftime("%Y-%m-%d"),
                }
            )
    if validated_params.filing_category:
        query_params["category"] = validated_params.filing_category
    elif validated_params.single_forms:
        query_params["category"] = "custom"
        query_params["forms"] = validated_params.single_forms
    if validated_params.peo_in:
        query_params["locationCode"] = PEO_IN_AND_INC_IN_TO_SEC_FORM_ID[
            validated_params.peo_in
        ]
    encoded_params = parse.urlencode(
        query_params, doseq=True, encoding="utf-8", quote_via=parse.quote
    )
    return parse.urljoin(base=base_url, url=encoded_params, allow_fragments=False)
