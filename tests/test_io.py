import json
import re

import pytest

from edgar_tool.io import write_results_to_file


@pytest.fixture
def data():
    return [
        {
            "root_form": "DEF 14A",
            "form_name": "Proxy statement",
            "filed_at": "2021-01-04",
            "reporting_for": "2021-02-15",
            "entity_name": "FINANCIAL INVESTORS TRUST",
            "ticker": None,
            "company_cik": "0000915802",
            "company_cik_trimmed": "915802",
            "place_of_business": "Denver, Colorado",
            "incorporated_location": "Delaware",
            "file_num": "811-08194",
            "file_num_search_url": "https://www.sec.gov/cgi-bin/browse-edgar/?filenum=811-08194&action=getcompany",
            "film_num": "21500495",
            "filing_details_url": "https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/0001398344-21-000011-index.html",
            "filing_document_url": "https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/fp0060683_def14a.htm",
        }
    ]


@pytest.fixture
def field_names():
    return [
        "root_form",
        "form_name",
        "filed_at",
        "reporting_for",
        "entity_name",
        "ticker",
        "company_cik",
        "company_cik_trimmed",
        "place_of_business",
        "incorporated_location",
        "file_num",
        "file_num_search_url",
        "film_num",
        "filing_details_url",
        "filing_document_url",
    ]


def test_write_results_to_csv(data, field_names, tmp_path):
    # GIVEN
    file_name = tmp_path / "results.csv"
    expected_result = """
root_form,form_name,filed_at,reporting_for,entity_name,ticker,company_cik,company_cik_trimmed,place_of_business,incorporated_location,file_num,file_num_search_url,film_num,filing_details_url,filing_document_url
DEF 14A,Proxy statement,2021-01-04,2021-02-15,FINANCIAL INVESTORS TRUST,,0000915802,915802,"Denver, Colorado",Delaware,811-08194,https://www.sec.gov/cgi-bin/browse-edgar/?filenum=811-08194&action=getcompany,21500495,https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/0001398344-21-000011-index.html,https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/fp0060683_def14a.htm
"""

    # WHEN
    write_results_to_file(data, str(file_name), field_names)
    actual_result = file_name.read_text().strip()

    # THEN
    assert actual_result == expected_result.strip()


def test_write_results_to_json(data, field_names, tmp_path):
    # GIVEN
    file_name = tmp_path / "results.json"
    expected_result = [
        {
            "root_form": "DEF 14A",
            "form_name": "Proxy statement",
            "filed_at": "2021-01-04",
            "reporting_for": "2021-02-15",
            "entity_name": "FINANCIAL INVESTORS TRUST",
            "ticker": None,
            "company_cik": "0000915802",
            "company_cik_trimmed": "915802",
            "place_of_business": "Denver, Colorado",
            "incorporated_location": "Delaware",
            "file_num": "811-08194",
            "file_num_search_url": "https://www.sec.gov/cgi-bin/browse-edgar/?filenum=811-08194&action=getcompany",
            "film_num": "21500495",
            "filing_details_url": "https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/0001398344-21-000011-index.html",
            "filing_document_url": "https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/fp0060683_def14a.htm",
        }
    ]

    # WHEN
    write_results_to_file(data, str(file_name), field_names)
    actual_result = json.loads(file_name.read_text().strip())

    # THEN
    assert actual_result == expected_result


def test_write_results_to_jsonlines(data, field_names, tmp_path):
    # GIVEN
    file_name = tmp_path / "results.jsonl"
    expected_result = {
        "root_form": "DEF 14A",
        "form_name": "Proxy statement",
        "filed_at": "2021-01-04",
        "reporting_for": "2021-02-15",
        "entity_name": "FINANCIAL INVESTORS TRUST",
        "ticker": None,
        "company_cik": "0000915802",
        "company_cik_trimmed": "915802",
        "place_of_business": "Denver, Colorado",
        "incorporated_location": "Delaware",
        "file_num": "811-08194",
        "file_num_search_url": "https://www.sec.gov/cgi-bin/browse-edgar/?filenum=811-08194&action=getcompany",
        "film_num": "21500495",
        "filing_details_url": "https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/0001398344-21-000011-index.html",
        "filing_document_url": "https://www.sec.gov/Archives/edgar/data/915802/000139834421000011/fp0060683_def14a.htm",
    }

    # WHEN
    write_results_to_file(data, str(file_name), field_names)
    actual_result = json.loads(file_name.read_text().strip())

    # THEN
    assert actual_result == expected_result


def test_write_results_to_file_with_unsupported_extension(data, field_names, tmp_path):
    # GIVEN
    file_name = tmp_path / "results.txt"
    expected_error_message = f"Unsupported file extension for destination file: {file_name} (should be one of .csv, .jsonl, .json)"

    # WHEN
    with pytest.raises(ValueError, match=re.escape(expected_error_message)):
        write_results_to_file(data, str(file_name), field_names)
