import subprocess


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
