from datetime import date, timedelta

from src.browser import create_browser_driver
from src.edgar import SecEdgarScraper

if __name__ == "__main__":
    words = ["Jeff Lawson"]
    company_name = None
    start = None
    end = None
    doc_category = "all_annual_quarterly_and_current_reports"
    is_exact_search = True
    browser_name = "chrome"
    with create_browser_driver(browser_name, headless=True) as driver:
        scraper = SecEdgarScraper(driver=driver)
        scraper.custom_text_search(
            search_keywords=words,
            entity_identifier=None,
            filing_category=None,
            exact_search=False,
            start_date=date.today() - timedelta(days=365 * 5),
            end_date=date.today(),
            wait_for_request_secs=8,
            stop_after_n=3,
        )
