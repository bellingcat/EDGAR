import datetime
from typing import Optional, Union
from urllib import parse

import pydantic
from dateutil.relativedelta import relativedelta

from edgar_tool import constants


class SearchParams(pydantic.BaseModel):
    keywords: Optional[list[str]] = None
    entity: Optional[str] = None
    filing_category: Optional[constants.FilingCategoryLiteral] = None
    single_forms: Optional[list[constants.FilingLiteral]] = None
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

    @property
    def keywords_formatted(self):
        """Returns the keywords to search for, wrapping exact phrases in quotes."""
        if not self.keywords:
            return None
        return [f'"{phrase}"' if " " in phrase else phrase for phrase in self.keywords]

    @property
    def start_date_formatted(self):
        if self.date_range_select == "all":
            return datetime.date(2001, 1, 1)
        elif self.date_range_select == "10y":
            return datetime.date.today() - relativedelta(years=10)
        elif self.date_range_select == "5y":
            return datetime.date.today() - relativedelta(years=5)
        elif self.date_range_select == "1y":
            return datetime.date.today() - relativedelta(years=1)
        elif self.date_range_select == "30d":
            return datetime.date.today() - datetime.timedelta(days=30)
        else:
            return self.start_date

    @property
    def end_date_formatted(self):
        if self.date_range_select in ["all", "10y", "5y", "1y", "30d"]:
            return datetime.date.today()
        else:
            return self.end_date

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
    def inc_in_formatted(self):
        return self._get_formatted_location(self.inc_in)

    @property
    def peo_in_formatted(self):
        return self._get_formatted_location(self.peo_in)

    @property
    def filing_category_formatted(self):
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
        return filing_category_to_sec_form_id.get(self.filing_category)


def generate_search_url_for_kwargs(search_params: SearchParams) -> str:
    query_params = {}
    if search_params.keywords:
        query_params["q"] = " ".join(search_params.keywords_formatted)
    if search_params.entity:
        query_params["entityName"] = search_params.entity
    if date_range_select := search_params.date_range_select:
        if date_range_select != "5y":
            query_params.update(
                {
                    "dateRange": date_range_select,
                }
            )
        query_params.update(
            {
                "startdt": search_params.start_date_formatted.strftime("%Y-%m-%d"),
                "enddt": search_params.end_date_formatted.strftime("%Y-%m-%d"),
            }
        )
    if search_params.single_forms:
        query_params["category"] = "custom"
        query_params["forms"] = ",".join(search_params.single_forms)
    elif search_params.filing_category_formatted:
        query_params["category"] = search_params.filing_category_formatted
    if search_params.peo_in:
        # The SEC API uses both locationCode and locationCodes for peo_in and inc_in
        query_params["locationCode"] = search_params.peo_in_formatted
        query_params["locationCodes"] = search_params.peo_in_formatted
    elif search_params.inc_in:
        query_params["locationType"] = "incorporated"
        query_params["locationCode"] = search_params.inc_in_formatted
        query_params["locationCodes"] = search_params.inc_in_formatted
    encoded_params = parse.urlencode(
        query_params, doseq=True, encoding="utf-8", quote_via=parse.quote
    )
    return constants.TEXT_SEARCH_BASE_URL + encoded_params
