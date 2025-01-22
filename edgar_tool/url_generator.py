import datetime
from typing import Optional, TypedDict, Union
from urllib import parse

import pydantic

from edgar_tool import constants


class _SearchQueryKwargsValidator(pydantic.BaseModel):
    keywords: Optional[list[str]] = None
    entity: Optional[str] = None
    filing_category: Optional[constants.FilingCategoryLiteral] = None
    single_forms: Optional[list[str]] = None
    date_range_select: Optional[constants.DateRangeLiteral] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    inc_in: Optional[
        Union[constants.LocationLiteral, list[constants.LocationLiteral]]
    ] = None
    peo_in: Optional[
        Union[constants.LocationLiteral, list[constants.LocationLiteral]]
    ] = None

    @pydantic.field_validator("inc_in", "peo_in", mode="before")
    def validate_location_code(cls, raw_location):
        if not raw_location:
            return raw_location
        value_error = ValueError(
            "Invalid location code. Please provide a valid 2-letter state abbreviation, "
            "3-letter country code, or 'XX' for unknown."
        )
        if (
            isinstance(raw_location, str)
            and raw_location not in constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID
        ):
            raise value_error
        if isinstance(raw_location, list):
            for loc in raw_location:
                if loc not in constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID:
                    raise value_error
        return raw_location

    @pydantic.model_validator(mode="after")
    def check_fields(self):
        if (
            not self.keywords
            and not self.entity
            and (not self.filing_category or self.filing_category == "all")
            and not self.single_forms
        ):
            raise ValueError(
                "Invalid search arguments. You must provide keywords, an entity, a filing category, "
                "or 1+ single forms. Filing category cannot be 'all'."
            )

        if not self.date_range_select and self.start_date and self.end_date:
            self.date_range_select = "custom"

        if self.date_range_select == "custom" and not (
            self.start_date and self.end_date
        ):
            raise ValueError(
                "Invalid date parameters. You must provide both a start and end date if searching a custom date range."
            )

        if (
            self.filing_category
            and self.filing_category != "custom"
            and self.single_forms
        ):
            raise ValueError(
                "Cannot specify both filing_category and single_forms. "
                "Passing single_forms automatically sets the filing_category to custom. "
                "Please choose one or the other."
            )

        if self.peo_in and self.inc_in:
            raise ValueError(
                "Cannot specify both peo_in and inc_in. Please choose one or the other."
            )

        return self


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


class _ValidSearchParams:
    def __init__(self, **query_args: SearchQueryKwargs):
        validated_params = _SearchQueryKwargsValidator(**query_args)

        self._keywords = validated_params.keywords
        self.entity = validated_params.entity
        self.date_range_select = (
            ""
            if validated_params.date_range_select == "5y"
            else validated_params.date_range_select
        )
        self._filing_category = validated_params.filing_category
        self.single_forms = validated_params.single_forms
        self.start_date = validated_params.start_date
        self.end_date = validated_params.end_date
        self._inc_in = validated_params.inc_in
        self._peo_in = validated_params.peo_in

    @property
    def keywords(self):
        return self._keywords

    @keywords.getter
    def keywords(self):
        """Returns the keywords to search for, wrapping exact phrases in quotes."""
        if not self._keywords:
            return None
        return [f'"{phrase}"' if " " in phrase else phrase for phrase in self._keywords]

    @staticmethod
    def _get_formatted_location(
        location: Union[constants.LocationLiteral, list[constants.LocationLiteral]]
    ) -> str:
        if not location:
            return None
        if isinstance(location, str):
            return constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID[location]
        else:
            return ",".join(
                [constants.PEO_IN_AND_INC_IN_TO_SEC_FORM_ID[loc] for loc in location]
            )

    @property
    def inc_in(self):
        return self._inc_in

    @inc_in.getter
    def inc_in(self):
        return self._get_formatted_location(self._inc_in)

    @property
    def peo_in(self):
        return self._peo_in

    @peo_in.getter
    def peo_in(self):
        return self._get_formatted_location(self._peo_in)

    @property
    def filing_category(self):
        filing_category_to_sec_form_id = {
            "all": "",
            "custom": "custom",
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
        if "," in validated_params.peo_in:
            query_params["locationCodes"] = validated_params.peo_in
        else:
            query_params["locationCode"] = validated_params.peo_in
    elif validated_params.inc_in:
        query_params["locationType"] = "incorporated"
        if "," in validated_params.inc_in:
            query_params["locationCodes"] = validated_params.inc_in
        else:
            query_params["locationCode"] = validated_params.inc_in
    encoded_params = parse.urlencode(
        query_params, doseq=True, encoding="utf-8", quote_via=parse.quote
    )
    return constants.TEXT_SEARCH_BASE_URL + encoded_params
