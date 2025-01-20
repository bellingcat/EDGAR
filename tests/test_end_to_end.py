"""
Tests the end-to-end functionality of the SecEdgarScraperCli class by making
real calls to the SEC Edgar website and asserting the output is as expected.
"""

import pytest
from typer.testing import CliRunner

import edgar_tool

runner = CliRunner()


@pytest.fixture
def output_file(tmp_path):
    return tmp_path / "results.csv"


def test_text_search_end_to_end(output_file):
    """
    Tests the end-to-end functionality of `SecEdgarScraperCli.text_search` by
    verifying a past search always produces the same result.
    """
    # GIVEN
    expected_result = """
root_form,form_name,filed_at,reporting_for,entity_name,ticker,company_cik,company_cik_trimmed,place_of_business,incorporated_location,file_num,film_num,file_num_search_url,filing_details_url,filing_document_url
DEF 14A,Proxy statement,2021-01-04,2021-02-15,FINANCIAL INVESTORS TRUST,,0000915802,915802,"Denver, Colorado",Delaware,811-08194,21500495,https://www.sec.gov/cgi-bin/browse-edgar/?filenum=811-08194&action=getcompany,https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/0001398344-21-000011-index.html,https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/fp0060683_def14a.htm
"""

    # WHEN
    runner.invoke(
        edgar_tool.cli.app,
        [
            "text-search",
            "John Doe",
            "--output",
            str(output_file),
            "--start-date",
            "2021-01-01",
            "--end-date",
            "2021-01-05",
        ],
    )

    # THEN
    assert output_file.read_text().strip() == expected_result.strip()


def test_rss_end_to_end(output_file):
    """
    Tests that `SecEdgarScraperCli.rss` successfully retrieves the RSS feed.
    Does not assert anything about the contents because they are liable to change.

    Note that RSS feeds are difficult to test because the precise output is expected
    to change over time. This test only checks that the process from cli to file save
    runs without errors and produces a csv file with the correct header.
    """
    # GIVEN
    expected_header = "company_name,cik,trimmed_cik,ticker,published_date,title,link,description,form,filing_date,file_number,accession_number,acceptance_date,period,assistant_director,assigned_sic,fiscal_year_end,xbrl_files\n"

    # WHEN
    runner.invoke(
        edgar_tool.cli.app,
        ["rss", "GOOG", "--output", str(output_file)],
    )  # simulates `edgar-tool rss "GOOG" --output "results.csv"`

    # THEN: Assert the first line of the file is the expected header
    assert output_file.read_text().startswith(expected_header)
