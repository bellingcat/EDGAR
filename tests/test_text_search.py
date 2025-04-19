import json
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest

from edgar_tool.text_search import (
    PageCheckFailedError,
    fetch_page,
    generate_search_urls,
)
from edgar_tool.url_generator import SearchParams


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {"test": "data"}
    return mock


@pytest.fixture
def url():
    return "https://example.com/api"


def test_fetch_page_success(mock_response, url):
    # GIVEN
    static_uuid = UUID("3263b52d-3f83-4f00-8adf-b20b8a28e8ad")
    expected_headers = {
        "User-Agent": f"BellingcatEDGARTool_{static_uuid} contact-tech@bellingcat.com"
    }

    # WHEN
    with (
        patch("requests.get", return_value=mock_response) as mock_get,
        patch("uuid.uuid4", return_value=static_uuid),
    ):
        result = fetch_page(url)

        # THEN
        mock_get.assert_called_once_with(url, headers=expected_headers)
        assert result == {"test": "data"}


def test_fetch_page_http_error(url):
    """Test fetch_page with non-200 status code."""
    # GIVEN
    mock_response = MagicMock()
    mock_response.status_code = 404

    # WHEN / THEN
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(
            PageCheckFailedError,
            match=f"Error for url {url}, with code {mock_response.status_code}",
        ):
            fetch_page(url)


def test_fetch_page_retry_on_failure(url):
    """Test that fetch_page retries on failure."""
    # GIVEN
    mock_response_success = MagicMock()
    mock_response_success.status_code = 200
    mock_response_success.json.return_value = {"test": "data"}

    mock_response_failure = MagicMock()
    mock_response_failure.status_code = 500

    with patch(
        "requests.get",
        side_effect=[
            mock_response_failure,
            mock_response_failure,
            mock_response_success,
        ],
    ) as mock_get:
        # WHEN
        result = fetch_page(url)

        # THEN
        assert mock_get.call_count == 3
        assert result == {"test": "data"}


@pytest.mark.parametrize(
    "response_file, expected_url_count",
    [
        ("0_hits.json", 1),
        ("100_hits.json", 1),
        ("9999_hits.json", 100),
    ],
)
def test_generate_search_urls_less_than_10_000_results(
    response_file, expected_url_count
):
    """Test that generate_search_urls yields the correct number of URLs for a given response.

    Due to SEC API constraints, each URL is only for 100 results, and a given search returns
    a maximum of 10,000 results. Therefore less than 10,000 results should yield one URL for 100
    results.
    """
    # GIVEN
    search_params = SearchParams(keywords=["test"])
    with open(Path(__file__).parent / "responses" / response_file) as f:
        mock_response = json.load(f)

    with patch(
        "edgar_tool.text_search.fetch_page",
        return_value=mock_response,
    ):
        # WHEN
        # Make sure we exhaust the generator by converting it to a list.
        # This calls it as many times as it can be called.
        urls = list(generate_search_urls(search_params))

        # THEN
        assert len(urls) == expected_url_count


def test_generate_search_urls_yields_correct_paginated_urls():
    """Test that generate_search_urls yields the correct URLs when it needs to paginate through
    more than 100 results.
    """
    # GIVEN
    search_params = SearchParams(keywords=["test"])
    response_files = ("101_hits.json", "1_hit.json")
    mock_responses = []
    for filename in response_files:
        with open(Path(__file__).parent / "responses" / filename) as f:
            mock_responses.append(json.load(f))

    expected_urls = [
        "https://efts.sec.gov/LATEST/search-index?q=test",
        "https://efts.sec.gov/LATEST/search-index?q=test&page=2&from=100",
    ]

    with patch(
        "edgar_tool.text_search.fetch_page",
        side_effect=mock_responses,
    ):
        # WHEN
        urls = list(str(url) for url in generate_search_urls(search_params))

        # THEN
        assert urls == expected_urls


def test_generate_search_urls_more_than_10_000_results():
    """Test that generate_search_urls yields the correct number of URLs when it needs to split
    the date range in half.

    The first request returns 10,000 results, which is the maximum the SEC returns for a given date range.
    `generate_search_urls` should then split the date range in half and make two new search queries. In this case
    we use 9999 results for the first date range and 100 results for the second date range, which should
    yield 101 URLs total (100 for 9999 results and 1 for the 100 results).
    """
    # GIVEN
    search_params = SearchParams(
        keywords=["test"], start_date="2022-01-01", end_date="2022-01-02"
    )
    response_files = ("10000_hits.json", "9999_hits.json", "100_hits.json")
    mock_responses = []
    for filename in response_files:
        with open(Path(__file__).parent / "responses" / filename) as f:
            mock_responses.append(json.load(f))
    expected_url_count = 101

    with patch(
        "edgar_tool.text_search.fetch_page",
        side_effect=mock_responses,
    ):
        # WHEN
        urls = list(generate_search_urls(search_params))

        # THEN
        assert len(urls) == expected_url_count


def test_generate_search_urls_10_000_results_for_single_day():
    """Test that generate_search_urls yields 100 URLs when the SEC returns 10,000 results for a single day.

    If the SEC returns 10,000 results for a single day, `generate_search_urls` should yield 100 URLs and not
    try to split the date range in half. This is because the SEC API does not allow us to search a date range
    that is smaller than 1 day.
    """
    # GIVEN
    search_params = SearchParams(
        keywords=["test"], start_date="2022-01-01", end_date="2022-01-01"
    )
    with open(Path(__file__).parent / "responses" / "10000_hits.json") as f:
        mock_response = json.load(f)

    expected_url_count = 100

    with patch(
        "edgar_tool.text_search.fetch_page",
        return_value=mock_response,
    ):
        # WHEN
        urls = list(generate_search_urls(search_params))

        # THEN
        assert len(urls) == expected_url_count
