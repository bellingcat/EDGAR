from unittest.mock import patch

import pytest
from typer.testing import CliRunner

import edgar_tool

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_edgar_text_searcher():
    with patch("edgar_tool.cli.EdgarTextSearcher"):
        yield


@pytest.fixture(autouse=True)
def mock_fetch_rss_feed():
    with patch("edgar_tool.cli.fetch_rss_feed"):
        yield


class TestTextSearch:
    def test_cli_should_return_help_string_when_passed_no_args(self):
        """
        Tests that running edgar without any arguments
        returns the CLI's help string and 0 exit code.
        """
        # GIVEN/WHEN
        result = runner.invoke(edgar_tool.cli.app, [])

        # THEN
        assert result.exit_code == 0
        assert "Usage: edgar [OPTIONS] COMMAND [ARGS]..." in result.output

    def test_no_text_fails(self):
        """
        Tests that calling without text argument fails
        """
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search"],
        )

        # THEN
        assert result.exit_code != 0
        assert "Missing argument 'TEXT...'." in result.output

    def test_with_text_passes(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example"],
        )

        # THEN
        assert result.exit_code == 0

    @pytest.mark.parametrize("extension", [("csv"), ("json"), ("json1")])
    def test_with_valid_output_file_extension_passes(self, extension):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--output", f"test.{extension}"],
        )

        # THEN
        assert result.exit_code == 0

    @pytest.mark.parametrize("extension", [("yaml"), ("nonsense"), ("blob")])
    def test_with_invalid_output_file_extension_fails(self, extension):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--output", f"test.{extension}"],
        )

        # THEN
        assert result.exit_code != 0

    @pytest.mark.parametrize("date_range", ["all", "10y", "5y", "1y", "30d"])
    def test_with_valid_date_range_passes(self, date_range):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--date-range", f"{date_range}"],
        )
        # THEN
        assert result.exit_code == 0

    def test_with_invalid_date_range_fails(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--date-range", f"100y"],
        )
        # THEN
        assert result.exit_code != 0

    def test_with_valid_start_and_end_dates_pass(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            [
                "text-search",
                "example",
                "--start-date",
                "2024-07-28",
                "--end-date",
                "2025-01-05",
            ],
        )
        # THEN
        assert result.exit_code == 0

    def test_with_start_date_after_end_date_fails(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            [
                "text-search",
                "example",
                "--start-date",
                "2025-01-01",
                "--end-date",
                "2024-07-28",
            ],
        )
        # THEN
        assert result.exit_code != 0
        assert "Start date cannot be later than end date." in result.output

    def test_with_start_date_but_no_end_date_passes(self):
        """The CLI implicitly uses today's date as the end date when
        --start-date is specified but --end-date is not. Therefore it
        is acceptable to specify only the start date."""
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--start-date", "2025-01-01"],
        )
        # THEN
        assert result.exit_code == 0

    def test_with_entity_id_passes(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--entity-id", "AAPL"],
        )
        # THEN
        assert result.exit_code == 0

    @pytest.mark.parametrize(
        "filing_category",
        [
            "all",
            "custom",
            "all_except_section_16",
            "all_annual_quarterly_and_current_reports",
            "all_section_16",
            "beneficial_ownership_reports",
            "exempt_offerings",
            "registration_statements",
            "filing_review_correspondence",
            "sec_orders_and_notices",
            "proxy_materials",
            "tender_offers_and_going_private_tx",
            "trust_indentures",
        ],
    )
    def test_with_filing_category_passes(self, filing_category):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            [
                "text-search",
                "example",
                "--filing-category",
                filing_category,
            ],
        )
        # THEN
        assert result.exit_code == 0

    def test_with_invalid_filing_category_fails(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--filing-category", "invalid_category"],
        )
        # THEN
        assert result.exit_code != 0

    def test_with_invalid_single_form_fails(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--single-form", "INVALID_FORM"],
        )
        # THEN
        assert result.exit_code != 0

    def test_with_invalid_peo_in_fails(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--principal-executive-offices-in", "INVALID"],
        )
        # THEN
        assert result.exit_code != 0

    def test_with_invalid_inc_in_fails(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["text-search", "example", "--incorporated-in", "INVALID"],
        )
        # THEN
        assert result.exit_code != 0


class TestRss:
    def test_with_no_tickers_fails(self):
        """
        Tests that calling rss command without tickers argument fails
        """
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["rss"],
        )

        # THEN
        assert result.exit_code != 0
        assert "Missing argument 'TICKERS...'" in result.output

    def test_with_tickers_passes(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["rss", "AAPL", "MSFT"],
        )

        # THEN
        assert result.exit_code == 0

    def test_csv_output_file_extension_passes(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["rss", "AAPL", "--output", f"test.csv"],
        )

        # THEN
        assert result.exit_code == 0

    @pytest.mark.parametrize("extension", [("yaml"), ("nonsense"), ("blob")])
    def test_invalid_output_file_extension_fails(self, extension):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["rss", "AAPL", "--output", f"test.{extension}"],
        )

        # THEN
        assert result.exit_code != 0

    def test_with_refresh_tickers_mapping_passes(self):
        # GIVEN/WHEN
        result = runner.invoke(
            edgar_tool.cli.app,
            ["rss", "AAPL", "--refresh-tickers-mapping"],
        )

        # THEN
        assert result.exit_code == 0
