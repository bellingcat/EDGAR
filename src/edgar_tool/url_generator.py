from urllib import parse

import pydantic

from edgar_tool import constants
from edgar_tool.search_params import SearchParams


def generate_search_url_for_kwargs(search_params: SearchParams) -> pydantic.HttpUrl:
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
    return pydantic.HttpUrl(constants.TEXT_SEARCH_BASE_URL + encoded_params)
