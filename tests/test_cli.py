import subprocess
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
    """Tests that running edgar-tool without any arguments returns the CLI's help string and 0 exit code."""
    # GIVEN
    expected_output = """
Usage: edgar-tool [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ rss           Fetch the latest RSS feed data for the given company tickers   │
│               and save it to either a CSV, JSON, or JSONLines file.          │
│ text-search   Perform a custom text search on the SEC EDGAR website and save │
│               the results to either a CSV, JSON, or JSONLines file.          │
╰──────────────────────────────────────────────────────────────────────────────╯

"""
    # Split the lines so we can strip off any trailing whitespace characters.
    # The subprocess output puts spaces after [ARGS]...
    expected_lines = [line.strip() for line in expected_output.splitlines()]

    # WHEN
    result = subprocess.run(["edgar-tool"], capture_output=True, text=True)
    actual_lines = [line.strip() for line in result.stdout.splitlines()]

    # THEN
    assert result.returncode == 0
    assert actual_lines == expected_lines


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


def test_text_search_negative_retries_fails():
    """
    Tests that passing a negative value for --retries fails
    """
    # GIVEN/WHEN
    result = runner.invoke(
        edgar_tool.cli.app,
        [
            "text-search",
            "example",
            "--retries",
            "-1",
        ],
    )

    # THEN
    assert result.exit_code != 0
    assert (
        "Invalid value for '--retries' / '-r': -1 is not in the range x>=0."
        in result.output
    )
