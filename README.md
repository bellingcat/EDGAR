# EDGAR

CLI tool and resources enabling efficient and consistent retrieval of corporate and financial data from the SEC. 

## What is EDGAR?

EDGAR is a database of corporate filings maintained by the United States Securities and Exchange Commission (SEC). 
These filings contain a wealth of quantitative and qualitative information on every legal entity that issues non-exempt securities in the United States. 
Whether you are looking to study the fundamentals of your favorite stocks, or to track the corporate webs weaved by a person or company of interest, EDGAR is the place to do it.

But there's a catch. 

To _programatically_ access EDGAR data in a consistent and reliable manner is a complex problem. 
Most people who have found solutions to this problem charge a fee for it, or only provide limited free access to the obtained data. 

This tool was initially developed as part of the Bellingcat Tech Fellowship program, we hope it helps you utilise this incredible, free resource.

## Installation

At the moment, the tool is not available on PyPI yet, hence you need to clone the repository and run the script manually.

```bash
# Clone the repository and move to the cloned directory
git clone https://github.com/bellingcat/EDGAR.git
cd EDGAR

# Create virtual environment and install the required dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Text Search all EDGAR Filings

### What is the EDGAR text search tool?

If you're interested in finding all the documents mentioning a certain person, company or phrase in the EDGAR database, you can do that via the [full text search page](https://www.sec.gov/edgar/search/#)

It isn't always easy to get the information you might need from the SEC, so this Python tool lets you download the search results to a file without having to go through all the pages of results by hand.

This is a command line tool that takes a search query, opens a web browser in the background, and downloads the search results into a CSV file that can be opened in a spreadsheet program (such as Excel).

### Features

#### Search parameters

Most search parameters from the EDGAR text search page are supported, including:
- `Document word or phrase` (mandatory)
- `Company name, ticker or CIK, or individual's name` (optional)
- `Filing category` (optional)
- `Filed from` and `Filed to` dates (optional)

Currently unsupported search parameters are:
- `Filed date ranges` (since the same behavior can be achieved with `Filed from` and `Filed to` dates)
- `Principal executive offices in` (though it could be added in the future by hardcoding the list of supported values)

#### Pagination

The tool supports pagination, and will automatically download all available search results.

In addition, it works around a limitation of the SEC website that only displays the first 10000 results,
by automatically splitting date ranges into smaller ones until the number of results is below 10000, ensuring
that all results are downloaded.

#### Output formats

Currently supported outputs formats are:
- CSV
- JSONLines (one JSON object per line)

Output format is determined by the file extension of the output file path. 
Accepted values are `.csv` and `.jsonl` (case-insensitive).

#### Browsers

Currently supported browsers are:
- Chrome (default)
- Firefox
- Edge
- Safari

#### Retries

The tool supports retries in case of failed requests. Retries can be configured with the `--retries` argument, and the wait time between retries will be a random number between `--min_wait` and `--max_wait` arguments.

### Example usage

```bash
# Display help message describing all supported arguments along with their usage, aliases and eventual default values (type q to exit)
python main.py text_search --help

# Basic usage (defaults to searching the last 5 years of records)
python main.py text_search John Doe

# Usage with date range and export to custom CSV file
python main.py text_search Tsunami Hazards --start_date "2021-01-01" --end_date "2021-12-31" --output "results.csv"

# More advanced usage specifying more arguments, with export to JSON
python main.py text_search Volcano Monitoring --start_date "2021-01-01" --end_date "2021-12-31" --exact_search --output "results.json"\
          --filing_type "all_annual_quarterly_and_current_reports" --entity_id "0001030717" \
          --min_wait 5.0 --max_wait 7.0 --retries 3 --browser "firefox" --headless
          
# Using aliases where supported and exporting to JSONLines
python main.py text_search Calabarzon -s "2021-01-01" -o "results.jsonl" -f "all_annual_quarterly_and_current_reports" -r 3 -b "firefox" -h
```

**Note**: combining text search parameters with `entity_id` parameter seems to increase the risk of failed requests
on the SEC page due to an apparent bug, we recommend to either avoid doing so (you can specify an empty string for search keywords using `""` and use only entity ID) or setting the number of retries accordingly if you do so.

## RSS Feed customized retrieval

### What is the RSS feed customized retrieval tool ?

The SEC also publish a live feed of filings, and this part of the tool lets you monitor particular tickers for new filings, so you can get to-the-minute updates.

The output is a CSV file containing the company and filings' metadata, which can be opened in a spreadsheet program (such as Excel).

### Features

#### Companies CIK to Ticker mapping

Since the RSS feed uses CIKs instead of tickers, the tool includes a mapping of CIKs to tickers, which is used to filter the feed by ticker.
This mapping is obtained from the [SEC website](https://www.sec.gov/files/company_tickers.json) and is updated on user request.

#### Periodic retrieval

The RSS feed data returns the last 200 filings and is updated every 10 minutes (which doesn't mean all tickers are updated every 10 minutes).
The tool can fetch the feed either once on-demand, or at regular intervals.

### Example usage

```bash
# Display help message describing all supported arguments along with their usage, aliases and eventual default values (type q to exit)
python main.py rss --help

# Basic one-off usage with export to CSV
python main.py rss "GOOG" --output "rss_feed.csv"

# Periodic usage specifying 10 minutes interval duration, with export to JSON
python main.py rss "AAPL" "GOOG" "MSFT" --output "rss_feed.json" --every_n_mins 10

# Same example as above, using aliases and exporting to JSONLines (.jsonl)
python main.py rss "AAPL" "GOOG" "MSFT" -o "rss_feed.jsonl" -e 10
```

## Table of Cleaned Financial Data

I've built a table containing most income statement, balance sheet, and cash flow statement data for every company traded publicly in the U.S. This table is updated periodically, and [available here for download as a .CSV file](https://edgar.marketinference.com/). You can open this file in Excel, use it as a data source for your own code, or use my simple Python script to access time series for the desired data points. 

The current table is created by the following method:

  - Monthly bulk download of all company facts data from EDGAR (this is the data set accessed by the official APIs)
  - Scraping of all calculation sheets related to each filing associated with a publicly traded company
  - Create a dictionary matching the most commonly used GAAP tags with a plain English term 
  - For a given company, for each year:
    - Determine what GAAP tags are listed under each cashflow / income / balance sheet headings (or whatever alternative terms the company happens to use) in the calculation sheet 
    - For each tag:
      - Obtain all the data associated with the tag in the company's bulk download folder for the desired year, and the preceding one 
      - Determine whether the data is duration or point in time
      - Identify quarterly and yearly values based on the time data associated with each data point
      - Recalculate all quarterly values if the reported ones are cumulative
      - Calculate Q4 value
      - Create cleaned and sorted time series
      - Isolate the value for the considered year (or calculate trailing twelve month value based on preceding four quarters for this year if the company hasn't reported yet)
    - For some particularly problematic data points such as debts I use addition between related data points to ensure consistency (this is why the debt amounts are not always perfectly accurate, but almost always in the ballpark)
    - Match the GAAP tags with their plain English term
    - Keep a database of orphan tags, and add them into the dictionary, manually
   
The quality of any programmatically produced financial dataset is not going to be as accurate or as complete as a S&P Global or Bloomberg subscription. The dataset I have created is of comparable accuracy to what you can find on Yahoo Finance, but spans a wider time frame, and is good enough for me to use in my own projects such as [Market Inference](https://www.marketinference.com/) and [Graham](https://graham.marketinference.com/info). 

I believe we can keep improving this dataset – with your help! Please report inconsistencies to me and I will do my best to improve the existing method. I also am designing an entirely new method that I will implement early next year, based on the scraping of tables embedded in yearly/quarterly reports. 
