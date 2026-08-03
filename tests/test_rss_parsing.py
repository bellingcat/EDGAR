import pytest

from edgar_tool.rss import parse_rss_feed_data

TICKERS_MAPPING = {"320193": ["AAPL"]}

XBRL_FILE_HTM = '<edgar:xbrlFile edgar:url="https://example.invalid/a.htm"/>'
XBRL_FILE_XSD = '<edgar:xbrlFile edgar:url="https://example.invalid/a.xsd"/>'


def _item(xbrl_files: str) -> str:
    return f"""
    <item>
      <title>8-K - EXAMPLE CORP</title>
      <link>https://example.invalid/a.htm</link>
      <description>8-K</description>
      <pubDate>Mon, 03 Aug 2026 16:30:00 EDT</pubDate>
      <edgar:xbrlFiling>
        <edgar:companyName>EXAMPLE CORP</edgar:companyName>
        <edgar:formType>8-K</edgar:formType>
        <edgar:filingDate>08/03/2026</edgar:filingDate>
        <edgar:cikNumber>0000320193</edgar:cikNumber>
        <edgar:accessionNumber>0000320193-26-000001</edgar:accessionNumber>
        <edgar:fileNumber>001-36743</edgar:fileNumber>
        <edgar:acceptanceDatetime>20260803163000</edgar:acceptanceDatetime>
        <edgar:period>20260803</edgar:period>
        <edgar:assistantDirector>Office of Technology</edgar:assistantDirector>
        <edgar:assignedSic>3571</edgar:assignedSic>
        <edgar:fiscalYearEnd>0927</edgar:fiscalYearEnd>
        <edgar:xbrlFiles>
          {xbrl_files}
        </edgar:xbrlFiles>
      </edgar:xbrlFiling>
    </item>
"""


def _feed(items: str) -> bytes:
    return (
        '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
        '<rss version="2.0" xmlns:edgar="https://www.sec.gov/Archives/edgar">\n'
        f"  <channel>\n    <title>Latest Filings</title>\n{items}  </channel>\n</rss>\n"
    ).encode()


class _FakeResponse:
    def __init__(self, content: bytes):
        self.content = content


@pytest.mark.parametrize(
    "item_count,xbrl_files,expected_xbrl_files",
    [
        pytest.param(
            2,
            f"{XBRL_FILE_HTM}\n{XBRL_FILE_XSD}",
            ["https://example.invalid/a.htm", "https://example.invalid/a.xsd"],
            id="many-items-many-files",
        ),
        pytest.param(
            1,
            f"{XBRL_FILE_HTM}\n{XBRL_FILE_XSD}",
            ["https://example.invalid/a.htm", "https://example.invalid/a.xsd"],
            id="single-item",
        ),
        pytest.param(
            2,
            XBRL_FILE_HTM,
            "https://example.invalid/a.htm",
            id="single-xbrl-file",
        ),
        pytest.param(
            1,
            XBRL_FILE_HTM,
            "https://example.invalid/a.htm",
            id="single-item-and-single-xbrl-file",
        ),
    ],
)
def test_parses_feeds_with_single_repeated_elements(
    item_count, xbrl_files, expected_xbrl_files
):
    """
    xmltodict collapses a single-element list into a plain dict, so a feed with exactly
    one <item>, or an item with exactly one <edgar:xbrlFile>, used to make the parser
    iterate over dict keys and drop every item.

    Note `xbrl_files` is a bare string rather than a one-element list when the filing has
    a single file, because `unpack_singleton_list` unwraps it on the way out.
    """
    # GIVEN
    response = _FakeResponse(_feed(_item(xbrl_files) * item_count))

    # WHEN
    rows = list(parse_rss_feed_data(response, ["AAPL"], TICKERS_MAPPING))

    # THEN
    assert len(rows) == item_count
    assert all(r["ticker"] == "AAPL" for r in rows)
    assert all(r["company_name"] == "EXAMPLE CORP" for r in rows)
    assert all(r["cik"] == "0000320193" for r in rows)
    assert all(r["xbrl_files"] == expected_xbrl_files for r in rows)
