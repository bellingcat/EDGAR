from src.browser import create_browser_driver
from src.edgar import SecEdgarScraper

if __name__ == "__main__":
    words = ["Goldman Sachs"]
    company_name = None
    start = None
    end = None
    doc_category = "all_annual_quarterly_and_current_reports"
    is_exact_search = True
    browser_name = "chrome"
    with create_browser_driver(browser_name, headless=False) as driver:
        scraper = SecEdgarScraper(driver=driver)
        scraper.custom_text_search(
            search_keywords=words,
            entity_identifier=company_name,
            filing_category=doc_category,
            exact_search=is_exact_search,
        )
