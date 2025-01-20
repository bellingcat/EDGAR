import datetime
from typing import Optional, TypedDict
from urllib import parse

from pydantic import BaseModel, field_validator

from edgar_tool import constants


class SearchQueryKwargs(TypedDict, total=False):
    keywords: list[str]
    entity: str
    filing_category: constants.FilingCategoryLiteral
    single_forms: list[str]
    date_range_select: constants.DateRangeLiteral
    start_date: datetime.date
    end_date: datetime.date
    inc_in: constants.LocationLiteral
    peo_in: constants.LocationLiteral


class _SearchQueryKwargsValidator(BaseModel):
    keywords: Optional[list[str]] = None
    entity: Optional[str] = None
    filing_category: Optional[constants.FilingCategoryLiteral] = None
    single_forms: Optional[list[str]] = None
    date_range_select: constants.DateRangeLiteral = "5y"
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    inc_in: constants.LocationLiteral = ""
    peo_in: constants.LocationLiteral = ""

    @field_validator("inc_in", "peo_in", mode="before")
    def validate_location_code(cls, location):
        if location not in constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID:
            raise ValueError(
                "Invalid location code. Please provide a valid 2-letter state abbreviation, 3-letter country code, or 'XX' for unknown."
            )
        return location


class _ValidSearchParams:
    def __init__(self, **query_args: SearchQueryKwargs):
        query_args = _SearchQueryKwargsValidator(**query_args)
        keywords = query_args.keywords
        entity = query_args.entity
        filing_category = query_args.filing_category
        single_forms = query_args.single_forms
        if (
            not keywords
            and not entity
            and (not filing_category or filing_category == "View all")
            and not single_forms
        ):
            raise ValueError(
                "Invalid search arguments. You must provide keywords, an entity, a filing category, or 1+ single forms. "
                "Filing category cannot be 'View all'."
            )
        date_range_select = query_args.date_range_select
        start_date = query_args.start_date
        end_date = query_args.end_date
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
            "5y",
            "1y",
            "30d",
            "custom",
        }:
            raise ValueError(
                (
                    "Invalid date_range_select. "
                    'Value must be one of "all", "10y", "5y", "1y", "30d", or "custom"'
                )
            )

        self._keywords = keywords
        self.entity = entity
        # 5y is the default date range, so we don't need to include it in the URL
        self.date_range_select = date_range_select if date_range_select != "5y" else ""

        if filing_category and filing_category != "Custom" and single_forms:
            raise ValueError(
                "Cannot specify both filing_category and single_forms. "
                "Passing single_forms automatically sets the filing_category"
                " to custom. Please choose one or the other."
            )

        self._filing_category = query_args.filing_category
        self.single_forms = query_args.single_forms
        self.start_date = query_args.start_date
        self.end_date = query_args.end_date

        peo_in = query_args.peo_in
        inc_in = query_args.inc_in
        if peo_in and inc_in:
            raise ValueError(
                "Cannot specify both peo_in and inc_in. Please choose one or the other."
            )
        if (
            peo_in
            and peo_in not in constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID
            or inc_in
            and inc_in not in constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID
        ):
            raise ValueError(
                (
                    "Invalid location code. "
                    "Please provide a valid 2-letter state abbreviation, "
                    "3-letter country code, or 'XX' for unknown."
                )
            )
        self.inc_in = inc_in
        self.peo_in = peo_in

    @property
    def keywords(self):
        return self._keywords

    @keywords.getter
    def keywords(self):
        """Returns the keywords to search for, wrapping exact phrases in quotes."""
        if not self._keywords:
            return None
        return [f'"{phrase}"' if " " in phrase else phrase for phrase in self._keywords]

    @property
    def filing_category(self):
        return self._filing_category

    @keywords.getter
    def filing_category(self):
        filing_category_to_sec_form_id = {
            "View all": "",
            "Custom": "custom",
            "Exclude insider equity awards, transactions, and ownership (Section 16 Reports)": "form-cat0",
            "All annual, quarterly, and current reports": "form-cat1",
            "Insider equity awards, transactions, and ownership (Section 16 Reports)": "form-cat2",
            "Beneficial Ownership Reports": "form-cat3",
            "Exempt Offerings": "form-cat4",
            "Registration statements and prospectuses": "form-cat5",
            "Filing review correspondence": "form-cat6",
            "SEC orders and notices": "form-cat7",
            "Proxy materials": "form-cat8",
            "Tender offers and going private transactions": "form-cat9",
            "Trust indentures filings": "form-cat10",
        }
        return filing_category_to_sec_form_id.get(self._filing_category)


def generate_search_url_for_kwargs(search_kwargs: SearchQueryKwargs) -> str:
    validated_params = _ValidSearchParams(**search_kwargs)
    query_params = {}
    if validated_params.keywords:
        query_params["q"] = validated_params.keywords
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
    if validated_params.single_forms:
        query_params["category"] = "custom"
        query_params["forms"] = validated_params.single_forms
    elif validated_params.filing_category:
        query_params["category"] = validated_params.filing_category
    if validated_params.peo_in:
        query_params["locationCode"] = constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID[
            validated_params.peo_in
        ]
    elif validated_params.inc_in:
        query_params["locationType"] = "incorporated"
        query_params["locationCode"] = constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID[
            validated_params.inc_in
        ]
    encoded_params = parse.urlencode(
        query_params, doseq=True, encoding="utf-8", quote_via=parse.quote
    )
    return constants.TEXT_SEARCH_BASE_URL + encoded_params
