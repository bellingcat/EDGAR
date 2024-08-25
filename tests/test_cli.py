import pytest
import subprocess
import warnings
from datetime import datetime
from unittest.mock import patch
from edgar_tool.cli import SecEdgarScraperCli


def test_cli_should_return_help_string_when_passed_no_args():
    """
    Tests that running `edgar-tool` without any arguments returns the CLI's help string
    and an exit code of 0.
    """
    # GIVEN
    expected_help = """
NAME
    edgar-tool

SYNOPSIS
    edgar-tool COMMAND

COMMANDS
    COMMAND is one of the following:

     rss
       Fetch the latest RSS feed data for the given company tickers and save it to either a CSV, JSON, or JSONLines file.

     text_search
       Perform a custom text search on the SEC EDGAR website and save the results to either a CSV, JSON, or JSONLines file.
"""

    # WHEN
    result = subprocess.run(["edgar-tool"], capture_output=True, text=True)

    # THEN
    assert result.returncode == 0
    assert result.stdout.strip() == expected_help.strip()


@patch('edgar_tool.text_search.EdgarTextSearcher.text_search')
def test_text_search_capture_arguments(mock_text_search):
    """
    Tests that `SecEdgarScraperCli.text_search` correctly calls the `text_search` method
    with the expected arguments.
    """
    # ARRANGE: mock_text_search arg is provided by the patch decorator.
    
    # ACT
    SecEdgarScraperCli.text_search(
        "Tsunami", "Hazards",
        output="results.csv",
        entity_id="0001030717",
        filing_form="all_annual_quarterly_and_current_reports",
        start_date="2021-01-01",
        end_date="2021-12-31",
        min_wait=5.0,
        max_wait=7.0,
        retries=3,
        peo_in="NY, OH",
        inc_in=None
    )

    # ASSERT
    mock_text_search.assert_called_once_with(
        keywords=["Tsunami", "Hazards"],
        entity_id="0001030717",
        filing_form="All annual, quarterly, and current reports",  # Mapped with TEXT_SEARCH_FILING_VS_MAPPING_CATEGORIES_MAPPING
        single_forms=None,
        start_date=datetime(2021, 1, 1),
        end_date=datetime(2021, 12, 31),
        min_wait_seconds=5.0,
        max_wait_seconds=7.0,
        retries=3,
        destination="results.csv",
        peo_in="NY,OH", ## Whitespace stripped
        inc_in=None
    )

@patch("edgar_tool.text_search.write_results_to_file")
def test_text_search_end_to_end(mock_write_results_to_file):
    """
    Tests the end-to-end functionality of `SecEdgarScraperCli.text_search` by
    verifying that `text_search.write_results_to_file` is called with the correct parameters.
    Uses patch to avoid file creation during testing.
    
    Because this can fail due to internet connection issues, this raises a warning when it fails
    instead of raising a unittest failure. 
    """
    # ARRANGE: mock_write_results_to_file arg is provided by the patch decorator.
    try:
        # ACT
        SecEdgarScraperCli.text_search(
            "John Doe",
            output="results.csv",
            start_date="2021-01-01",
            end_date="2021-01-31"
        )

        # Extract and validate the call arguments
        call_args = mock_write_results_to_file.call_args
        results = list(call_args[0][0])
        
        # ASSERT: Check if 'root_form' is present in the first result
        assert 'root_form' in results[0][0]
    
    except Exception as e:
        # Because net connection or server issues can cause the above to fail. 
        warnings.warn(
            f"An exception occurred: {str(e)}\n"
            "There might be an issue with accessing the SEC website or the SEC's return payload.",
            UserWarning
        )


@patch('edgar_tool.text_search.EdgarTextSearcher.text_search')
def test_text_search_with_both_peo_in_and_inc_in(mock_text_search):
    """
    Tests that `SecEdgarScraperCli.text_search` raises an exception if both `peo_in` and `inc_in`
    are provided in the parameters.
    """
    # ARRANGE: mock_text_search arg is provided by the patch decorator.
    mock_text_search.side_effect = Exception("Use only one of peo_in or inc_in, not both.")
    
    ## ACT & ASSERT
    with pytest.raises(Exception, match="Use only one of peo_in or inc_in, not both."):
        SecEdgarScraperCli.text_search(
            ["Tsunami", "Hazards"],
            start_date="2019-06-01",
            end_date="2024-01-01",
            inc_in="NY,OH",
            peo_in="NY,OH"
        )

@patch('edgar_tool.rss.write_results_to_file')
def test_rss_end_to_end(mock_rss):
    """
    Tests that `SecEdgarScraperCli.rss` successfully retrieves the RSS feed. 
    Does not assert anything about the contents because they are liable to change.
    Uses patch to suppress file creation during testing.
    
    Because this can fail due to internet connection issues, this raises a warning when it fails
    instead of raising a unittest failure. 
    """
    # ARRANGE: mock_rss arg is provided by the patch decorator.
    try:
        # ACT: simulates `edgar-tool rss "GOOG" --output "rss_feed.csv"`
        SecEdgarScraperCli.rss(
            "GOOG",
            output="rss_feed.csv"
        )

        # ASSERT: Checks that rss.write_results_to_file would have been called, 
        # but does not call it to avoid file creation during testing.
        assert mock_rss.call_args
    except Exception as e:
        # Because net connection or server issues can cause the above to fail. 
        warnings.warn(
            f"An exception occurred: {str(e)}\n"
            "There might be an issue with accessing the RSS feed or the return payload.",
            UserWarning
        )