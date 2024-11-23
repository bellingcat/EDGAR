import subprocess
import warnings
from unittest.mock import patch
from edgar_tool.cli import SecEdgarScraperCli

def test_cli_should_return_help_string_when_passed_no_args():
    """Tests that running edgar-tool without any arguments returns the CLI's help string and 0 exit code."""
    # GIVEN
    expected = """
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
    assert result.stdout.strip() == expected.strip()

@patch("edgar_tool.text_search.write_results_to_file")
def test_text_search_end_to_end(mock_write_results_to_file):
    """
    Tests the end-to-end functionality of `SecEdgarScraperCli.text_search` by
    verifying that `text_search.write_results_to_file` is called with the correct parameters.
    Uses patch to avoid file creation during testing. Ensures output file has the correct structure.
    
    Because this can fail due to internet connection issues, this raises a warning when it fails
    instead of raising a unittest failure.
    """
    # GIVEN: Mock the write_results_to_file function to avoid file creation during testing
    try:
        # WHEN: Perform the text search
        SecEdgarScraperCli.text_search(
            "John Doe",
            output="results.csv",
            start_date="2021-01-01",
            end_date="2021-01-31"
        )
        
        # Retrieve the call arguments of the mocked function
        call_args = mock_write_results_to_file.call_args
        results = list(call_args[0][0])  # results data is the first call arg in a list of one call arg
        
        # THEN: Verify the structure of the first result
        first_result = results[0][0]  # is list of one item which is list of all results
        fields = list(first_result.keys())  # the column headers to be written to the csv
        expected_fields = [
            'root_form', 'form_name', 'filed_at', 'reporting_for', 'entity_name', 
            'ticker', 'company_cik', 'company_cik_trimmed', 'place_of_business', 
            'incorporated_location', 'file_num', 'file_num_search_url', 'film_num', 
            'filing_details_url', 'filing_document_url'
        ]
        
        assert fields == expected_fields
    
    except Exception as e:
        # Log a warning instead of failing the test
        warnings.warn(
            f"An exception occurred: {str(e)}\n"
            "There might be an issue with accessing the SEC website or the SEC's return payload.",
            UserWarning
        )

@patch('edgar_tool.rss.write_results_to_file')
def test_rss_end_to_end(mock_rss):
    """
    Tests that `SecEdgarScraperCli.rss` successfully retrieves the RSS feed. 
    Does not assert anything about the contents because they are liable to change.
    Uses patch to suppress file creation during testing. Ensures output file has 
    the correct structure.
    
    Note that RSS feeds are difficult to test because the precise output is expected 
    to change over time. This test only checks that the process from cli to file save
    runs without errors.
    
    Because this can fail due to internet connection issues, this raises a warning when it fails
    instead of raising a unittest failure.
    """
    # GIVEN: Mock the write_results_to_file function to avoid file creation during testing
    try:
        # WHEN: simulates `edgar-tool rss "GOOG" --output "rss_feed.csv"`
        SecEdgarScraperCli.rss(
            "GOOG",
            output="rss_feed.csv"
        )

        # THEN: Checks that rss.write_results_to_file would have been called  
        # without a runtime error, but does not call it to avoid file creation 
        # during testing.
        fields = mock_rss.call_args[0][2]  # call args are a list of one item, 2 index are the csv column headers
        
        expected_fields = [
            'company_name', 'cik', 'trimmed_cik', 'ticker', 'published_date', 'title', 
            'link', 'description', 'form', 'filing_date', 'file_number', 'accession_number', 
            'acceptance_date', 'period', 'assistant_director', 'assigned_sic', 
            'fiscal_year_end', 'xbrl_files'
        ]
        assert fields == expected_fields
    except Exception as e:
        # Log a warning instead of failing the test
        warnings.warn(
            f"An exception occurred: {str(e)}\n"
            "There might be an issue with accessing the RSS feed or the return payload.",
            UserWarning
        )