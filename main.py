import json

from src.browser import (
    create_browser_driver,
)
from src.edgar import custom_text_search

if __name__ == "__main__":
    words = ["jeff lawson"]
    company_name = None
    start = None
    end = None
    doc_category = "all_annual_quarterly_and_current_reports"
    is_exact_search = True
    browser_name = "chrome"
    browser = create_browser_driver(browser_name, headless=False)
    print(f"{browser_name.capitalize()} browser successfully created")
    results = custom_text_search(
        driver=browser,
        search_keywords=words,
        entity_identifier=company_name,
        filing_category=doc_category,
        exact_search=is_exact_search,
    )
    print(json.dumps(results, indent=4, sort_keys=True, default=str))
