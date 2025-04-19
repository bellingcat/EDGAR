from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest

from edgar_tool.text_search import PageCheckFailedError, fetch_page


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
