import time
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date, timedelta
from typing import List, Dict, Optional, Any, Union
import requests
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.webdriver import WebDriver as EdgeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.ie.webdriver import WebDriver as IeWebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver

from src.constants import BASE_URL, FILING_CATEGORIES_MAPPING


def create_browser_driver(browser_name: str) -> Union[ChromeWebDriver, SafariWebDriver, FirefoxWebDriver, EdgeWebDriver, IeWebDriver]:

    """
    Creates a Selenium WebDriver based on the given browser name, fails with a ValueError if the browser name is not supported.

    :param browser_name: name of the browser to create the WebDriver for, should be one of "chrome", "safari", "firefox", "edge", or "ie"
    :return: the created WebDriver
    """

    if browser_name == "chrome":
        return webdriver.Chrome()
    elif browser_name == "safari":
        return webdriver.Safari()
    elif browser_name == "firefox":
        return webdriver.Firefox()
    elif browser_name == "edge":
        return webdriver.Edge()
    elif browser_name == "ie":
        return webdriver.Ie()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")


def custom_text_search(driver: Union[ChromeWebDriver, SafariWebDriver, FirefoxWebDriver, EdgeWebDriver, IeWebDriver],
                       search_keywords: List[str],
                       entity_identifier: Optional[str] = None,
                       filing_category: Optional[str] = None,
                       exact_search: bool = False,
                       start_date: date = date.today() - timedelta(days=365*5),
                       end_date: date = date.today()) -> None:

    """
    Searches the SEC website for filings based on the given parameters.

    :param driver: Selenium WebDriver
    :param search_keywords: Search keywords to input in the "Document word or phrase" field
    :param entity_identifier: Entity/Person name, ticker, or CIK number to input in the "Company name, ticker, or CIK" field
    :param filing_category: Filing category to select from the dropdown menu, defaults to None
    :param exact_search: Whether to perform an exact search on the search_keywords argument or not, defaults to False in order to return the maximum amount of search results by default
    :param start_date: Start date for the custom date range, defaults to 5 years ago to replicate the default behavior of the SEC website
    :param end_date: End date for the custom date range, defaults to current date in order to replicate the default behavior of the SEC website
    :return:
    """

    search_keywords = " ".join(search_keywords)
    search_keywords = f'"{search_keywords}"' if exact_search else search_keywords
    request_args = {
        "q": urllib.parse.quote(search_keywords),
        "dateRange": "custom",
        "startdt": start_date.strftime("%Y-%m-%d"),
        "enddt": end_date.strftime("%Y-%m-%d"),
    }

    if entity_identifier:
        request_args["entityName"] = entity_identifier

    if filing_category:
        request_args["category"] = FILING_CATEGORIES_MAPPING[filing_category]

    request_args = urllib.parse.urlencode(request_args)
    url = f"{BASE_URL}{request_args}"
    print(f"Requesting URL: {url}")
    driver.get(url)
    print(f"Successfully fetched URL: {url}")
    table = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/table/tbody").find_elements(By.TAG_NAME, "tr")
    for row in table:
        print(row.find_elements(By.TAG_NAME, "td"))


if __name__ == "__main__":
    words = ["jeff", "lawson"]
    company_name = "twilio"
    start = None
    end = None
    doc_category = "all_annual_quarterly_and_current_reports"
    is_exact_search = True
    browser_name = "chrome"
    browser = create_browser_driver(browser_name)
    print(f"{browser_name.capitalize()} browser successfully created")
    custom_text_search(driver=browser,
                       search_keywords=words,
                       entity_identifier=company_name,
                       filing_category=doc_category,
                       exact_search=is_exact_search)
