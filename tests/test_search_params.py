import datetime
import re
from typing import Literal

import pytest
from dateutil.relativedelta import relativedelta

from edgar_tool.search_params import SearchParams


class TestSearchParamsValidation:
    def test_should_raise_if_no_search_criteria_provided(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Invalid search arguments. You must provide keywords, an entity, a filing category, "
                "or 1+ single forms. Filing category cannot be 'all'."
            ),
        ):
            SearchParams()

    def test_should_raise_if_filing_category_is_all(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Invalid search arguments. You must provide keywords, an entity, a filing category, "
                "or 1+ single forms. Filing category cannot be 'all'."
            ),
        ):
            SearchParams(filing_category="all")

    def test_should_raise_if_custom_date_range_missing_dates(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Invalid date parameters. You must provide both a start and end date if searching a custom date range."
            ),
        ):
            SearchParams(
                keywords=["test"],
                date_range_select="custom",
                start_date=datetime.date(2020, 1, 1),
            )

    def test_should_raise_if_both_filing_category_and_single_forms(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Cannot specify both filing_category and single_forms. "
                "Passing single_forms automatically sets the filing_category to custom. "
                "Please choose one or the other."
            ),
        ):
            SearchParams(
                filing_category="beneficial_ownership_reports",
                single_forms=["4"],
            )

    def test_should_raise_if_both_peo_in_and_inc_in(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Cannot specify both peo_in and inc_in. Please choose one or the other."
            ),
        ):
            SearchParams(
                keywords=["test"],
                peo_in="CA",
                inc_in="CA",
            )

    def test_should_raise_if_invalid_location_code(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Invalid location code. Please provide a valid 2-letter state abbreviation, "
                "3-letter country code, or 'XX' for unknown."
            ),
        ):
            SearchParams(keywords=["test"], peo_in="INVALID")


class TestSearchParamsProperties:
    @pytest.mark.parametrize(
        "keywords,expected",
        [
            (["single"], ["single"]),
            (["multiple words"], ['"multiple words"']),
            (["single", "multiple words"], ["single", '"multiple words"']),
        ],
    )
    def test_keywords_formatted(self, keywords: list[str], expected: list[str]):
        # GIVEN
        search_params = SearchParams(keywords=keywords)

        # WHEN
        result = search_params.keywords_formatted

        # THEN
        assert result == expected

    @pytest.mark.parametrize(
        "date_range_select,expected",
        [
            ("all", datetime.date(2001, 1, 1)),
            ("10y", datetime.date.today() - relativedelta(years=10)),
            ("5y", datetime.date.today() - relativedelta(years=5)),
            ("1y", datetime.date.today() - relativedelta(years=1)),
            ("30d", datetime.date.today() - datetime.timedelta(days=30)),
        ],
    )
    def test_start_date_formatted(
        self,
        date_range_select: (
            Literal["all"]
            | Literal["10y"]
            | Literal["5y"]
            | Literal["1y"]
            | Literal["30d"]
        ),
        expected: datetime.date,
    ):
        # GIVEN
        search_params = SearchParams(
            keywords=["test"],
            date_range_select=date_range_select,
        )

        # WHEN
        result = search_params.start_date_formatted

        # THEN
        assert result == expected

    @pytest.mark.parametrize(
        "date_range_select,expected",
        [
            ("all", datetime.date.today()),
            ("10y", datetime.date.today()),
            ("5y", datetime.date.today()),
            ("1y", datetime.date.today()),
            ("30d", datetime.date.today()),
        ],
    )
    def test_end_date_formatted(
        self,
        date_range_select: (
            Literal["all"]
            | Literal["10y"]
            | Literal["5y"]
            | Literal["1y"]
            | Literal["30d"]
            | Literal["custom"]
        ),
        expected: datetime.date,
    ):
        # GIVEN
        search_params = SearchParams(
            keywords=["test"],
            date_range_select=date_range_select,
        )

        # WHEN
        result = search_params.end_date_formatted

        # THEN
        assert result == expected

    @pytest.mark.parametrize(
        "date_range_select",
        ["all", "10y", "5y", "1y", "30d"],
    )
    def test_date_range_select_custom_cannot_be_used_with_start_date(
        self,
        date_range_select: Literal["all", "10y", "5y", "1y", "30d"],
    ):
        # GIVEN / WHEN / THEN
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Cannot specify both date_range_select and start_date if "
                "date_range_select is not 'custom'. date_range_select assumes "
                "the end date is today and calculates the start date based on the date range."
            ),
        ):
            SearchParams(
                keywords=["test"],
                date_range_select=date_range_select,
                start_date=datetime.date(2024, 6, 1),
            )

    def test_date_range_select_custom_with_start_date_and_end_date(self):
        # GIVEN
        start_date = datetime.date(2024, 6, 1)
        end_date = datetime.date(2024, 6, 30)

        # WHEN
        search_params = SearchParams(
            keywords=["test"],
            date_range_select="custom",
            start_date=start_date,
            end_date=end_date,
        )

        # THEN
        assert search_params.date_range_select == "custom"
        assert search_params.start_date_formatted == start_date
        assert search_params.end_date_formatted == end_date

    @pytest.mark.parametrize(
        "location,expected",
        [
            (None, None),
            ("CA", "CA"),
            (["CA", "NY"], "CA,NY"),
        ],
    )
    def test_inc_in_formatted(
        self,
        location: None | list[str] | Literal["CA"],
        expected: None | Literal["CA"] | Literal["CA,NY"],
    ):
        # GIVEN
        search_params = SearchParams(keywords=["test"], inc_in=location)

        # WHEN
        result = search_params.inc_in_formatted

        # THEN
        assert result == expected

    @pytest.mark.parametrize(
        "location,expected",
        [
            (None, None),
            ("CA", "CA"),
            (["CA", "NY"], "CA,NY"),
        ],
    )
    def test_peo_in_formatted(
        self,
        location: None | list[str] | Literal["CA"],
        expected: None | Literal["CA"] | Literal["CA,NY"],
    ):
        # GIVEN
        search_params = SearchParams(keywords=["test"], peo_in=location)

        # WHEN
        result = search_params.peo_in_formatted

        # THEN
        assert result == expected

    @pytest.mark.parametrize(
        "filing_category,expected",
        [
            ("all", ""),
            ("custom", "custom"),
            ("all_except_section_16", "form-cat0"),
            ("all_annual_quarterly_and_current_reports", "form-cat1"),
            ("all_section_16", "form-cat2"),
            ("beneficial_ownership_reports", "form-cat3"),
            ("exempt_offerings", "form-cat4"),
            ("registration_statements", "form-cat5"),
            ("filing_review_correspondence", "form-cat6"),
            ("sec_orders_and_notices", "form-cat7"),
            ("proxy_materials", "form-cat8"),
            ("tender_offers_and_going_private_tx", "form-cat9"),
            ("trust_indentures", "form-cat10"),
        ],
    )
    def test_filing_category_formatted(
        self,
        filing_category: (
            Literal["all"]
            | Literal["custom"]
            | Literal["all_except_section_16"]
            | Literal["all_annual_quarterly_and_current_reports"]
            | Literal["all_section_16"]
            | Literal["beneficial_ownership_reports"]
            | Literal["exempt_offerings"]
            | Literal["registration_statements"]
            | Literal["filing_review_correspondence"]
            | Literal["sec_orders_and_notices"]
            | Literal["proxy_materials"]
            | Literal["tender_offers_and_going_private_tx"]
            | Literal["trust_indentures"]
        ),
        expected: (
            Literal[""]
            | Literal["custom"]
            | Literal["form-cat0"]
            | Literal["form-cat1"]
            | Literal["form-cat2"]
            | Literal["form-cat3"]
            | Literal["form-cat4"]
            | Literal["form-cat5"]
            | Literal["form-cat6"]
            | Literal["form-cat7"]
            | Literal["form-cat8"]
            | Literal["form-cat9"]
            | Literal["form-cat10"]
        ),
    ):
        # GIVEN
        search_params = SearchParams(
            keywords=["test"],
            filing_category=filing_category,
        )

        # WHEN
        result = search_params.filing_category_formatted

        # THEN
        assert result == expected
