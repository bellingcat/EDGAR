import csv
import json
from unittest.mock import patch

import pytest

from edgar_tool.rss import fetch_rss_feed

RSS_XML = b"""<?xml version="1.0" encoding="ISO-8859-1"?>
<rss version="2.0" xmlns:edgar="https://www.sec.gov/Archives/edgar">
  <channel>
    <title>Latest Filings</title>
    <item>
      <title>8-K - EXAMPLE CORP (0000320193) (Filer)</title>
      <link>https://www.sec.gov/Archives/edgar/data/320193/000032019326000001.htm</link>
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
          <edgar:xbrlFile edgar:url="https://www.sec.gov/Archives/edgar/data/320193/a.htm"/>
          <edgar:xbrlFile edgar:url="https://www.sec.gov/Archives/edgar/data/320193/a.xsd"/>
        </edgar:xbrlFiles>
      </edgar:xbrlFiling>
    </item>
    <item>
      <title>10-Q - OTHER CORP (0000789019) (Filer)</title>
      <link>https://www.sec.gov/Archives/edgar/data/789019/000078901926000002.htm</link>
      <description>10-Q</description>
      <pubDate>Mon, 03 Aug 2026 17:00:00 EDT</pubDate>
      <edgar:xbrlFiling>
        <edgar:companyName>OTHER CORP</edgar:companyName>
        <edgar:formType>10-Q</edgar:formType>
        <edgar:filingDate>08/03/2026</edgar:filingDate>
        <edgar:cikNumber>0000789019</edgar:cikNumber>
        <edgar:accessionNumber>0000789019-26-000002</edgar:accessionNumber>
        <edgar:fileNumber>001-37845</edgar:fileNumber>
        <edgar:acceptanceDatetime>20260803170000</edgar:acceptanceDatetime>
        <edgar:period>20260630</edgar:period>
        <edgar:assistantDirector>Office of Technology</edgar:assistantDirector>
        <edgar:assignedSic>7372</edgar:assignedSic>
        <edgar:fiscalYearEnd>0630</edgar:fiscalYearEnd>
        <edgar:xbrlFiles>
          <edgar:xbrlFile edgar:url="https://www.sec.gov/Archives/edgar/data/789019/b.htm"/>
          <edgar:xbrlFile edgar:url="https://www.sec.gov/Archives/edgar/data/789019/b.xsd"/>
        </edgar:xbrlFiles>
      </edgar:xbrlFiling>
    </item>
  </channel>
</rss>
"""


class _FakeResponse:
    content = RSS_XML

    def raise_for_status(self):
        return None


@pytest.fixture
def rss_env(tmp_path):
    """Point the RSS module at a temp data dir and stub out both network calls."""
    tickers_file = tmp_path / "company_tickers.json"
    tickers_file.write_text(json.dumps({"320193": ["AAPL"], "789019": ["MSFT"]}))

    with (
        patch("edgar_tool.rss.RSS_FEED_DATA_DIRECTORY", tmp_path),
        patch("edgar_tool.rss.RSS_COMPANY_TICKERS_FILE_PATH", tickers_file),
        patch("edgar_tool.rss._fetch_company_tickers"),
        patch("edgar_tool.rss.requests.get", return_value=_FakeResponse()),
    ):
        yield


def test_fetch_rss_feed_writes_parsed_rows_to_csv(rss_env, tmp_path):
    """
    Regression test: fetch_rss_feed used to wrap its already-flat generator of row
    dicts in a second generator, so csv.DictWriter.writerows received a generator
    where it expects a mapping and raised
    `AttributeError: 'generator' object has no attribute 'keys'`.
    """
    # GIVEN
    output_file = tmp_path / "rss.csv"

    # WHEN
    fetch_rss_feed(["AAPL"], str(output_file), refresh_tickers_mapping=False)

    # THEN
    rows = list(csv.DictReader(output_file.open()))
    assert len(rows) == 1
    assert rows[0]["ticker"] == "AAPL"
    assert rows[0]["company_name"] == "EXAMPLE CORP"
    assert rows[0]["form"] == "8-K"
    assert rows[0]["cik"] == "0000320193"
    assert rows[0]["trimmed_cik"] == "320193"


def test_fetch_rss_feed_filters_out_non_matching_tickers(rss_env, tmp_path):
    # GIVEN
    output_file = tmp_path / "rss.csv"

    # WHEN
    fetch_rss_feed(["TSLA"], str(output_file), refresh_tickers_mapping=False)

    # THEN
    assert list(csv.DictReader(output_file.open())) == []
