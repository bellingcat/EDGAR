from unittest.mock import patch

import pytest
from typer.testing import CliRunner

import edgar_tool

runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_edgar_text_searcher():
    with patch("edgar_tool.cli.EdgarTextSearcher"):
        yield


def test_cli_should_return_help_string_when_passed_no_args():
    """
    Tests that running edgar-tool without any arguments
    returns the CLI's help string and 0 exit code.
    """
    # GIVEN/WHEN
    result = runner.invoke(edgar_tool.cli.app, [])

    # THEN
    assert result.exit_code == 0
    assert "Usage: edgar-tool [OPTIONS] COMMAND [ARGS]..." in result.output


def test_text_search_no_text_fails():
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


def test_text_search_with_text_passes():
    # GIVEN/WHEN
    result = runner.invoke(
        edgar_tool.cli.app,
        ["text-search", "example"],
    )

    # THEN
    assert result.exit_code == 0


@pytest.mark.parametrize("extension", [("csv"), ("json"), ("json1")])
def test_text_search_with_valid_output_file_extension_passes(extension):
    # GIVEN/WHEN
    result = runner.invoke(
        edgar_tool.cli.app,
        ["text-search", "example", "--output", f"test.{extension}"],
    )

    # THEN
    assert result.exit_code == 0


@pytest.mark.parametrize("extension", [("yaml"), ("nonsense"), ("blob")])
def test_text_search_with_invalid_output_file_extension_fails(extension):
    # GIVEN/WHEN
    result = runner.invoke(
        edgar_tool.cli.app,
        ["text-search", "example", "--output", f"test.{extension}"],
    )

    # THEN
    assert result.exit_code != 0


@pytest.mark.parametrize("date_range", ["all", "10y", "5y", "1y", "30d"])
def test_text_search_with_valid_date_range_passes(date_range):
    # GIVEN/WHEN
    result = runner.invoke(
        edgar_tool.cli.app,
        ["text-search", "example", "--date-range", f"{date_range}"],
    )
    # THEN
    assert result.exit_code == 0


def test_text_search_with_invalid_date_range_fails():
    # GIVEN/WHEN
    result = runner.invoke(
        edgar_tool.cli.app,
        ["text-search", "example", "--date-range", f"100y"],
    )
    # THEN
    assert result.exit_code != 0


def test_text_search_with_valid_start_and_end_dates_pass():
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


def test_text_search_with_start_date_after_end_date_fails():
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


def test_text_search_with_start_date_but_no_end_date_passes():
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
