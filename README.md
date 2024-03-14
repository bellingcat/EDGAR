# EDGAR

Python tool to search and retrieve corporate and financial data from the United States Securities and Exchange Commission (SEC). 

## What is EDGAR? 

EDGAR is a database of corporate filings maintained by the SEC. 
These filings contain a wealth of quantitative and qualitative information on every legal entity that issues non-exempt securities in the United States. 
Whether you are looking to study the fundamentals of your favorite stocks, or to track the corporate webs weaved by a person or company of interest, EDGAR is the place to do it.

This tool was initially developed as part of the Bellingcat Tech Fellowship program, we hope it helps you utilise this incredible, free resource.

## Installation :magic_wand:

[![PyPI - Version](https://img.shields.io/pypi/v/edgar-tool)
](https://pypi.org/project/edgar-tool/)

You can install this tool directly from the [official PyPi release](https://pypi.org/project/edgar-tool/).

```bash
pip install edgar-tool
```

## Usage - Text Search :mag_right:

### What is the text search tool?

If you're interested in finding all the documents mentioning a certain person, company or phrase in the EDGAR database, you can do that via the [full text search page](https://www.sec.gov/edgar/search/#)

It isn't always easy to get the information you might need from the SEC, so this Python tool lets you download the search results to a file without having to go through all the pages of results by hand.

This is a command line tool that takes a search query, opens a web browser in the background, and downloads the search results into a CSV file that can be opened in a spreadsheet program (such as Excel).

### Examples

```bash
# Display help message describing all supported arguments along with their usage, aliases and eventual default values (type q to exit)
edgar-tool text_search --help

# Basic usage (defaults to searching the last 5 years of records)
edgar-tool text_search John Doe

# Basic usage with a combination of exact and partial search parameters
edgar-tool text_search \"John Doe\" Pharmaceuticals Chemicals

# Usage with date range and export to custom CSV file
edgar-tool text_search Tsunami Hazards --start_date "2021-01-01" --end_date "2021-12-31" --output "results.csv"

# More advanced usage specifying more arguments, with export to JSON
edgar-tool text_search Volcano Monitoring --start_date "2021-01-01" --end_date "2021-12-31" --output "results.json"\
          --filing_type "all_annual_quarterly_and_current_reports" --entity_id "0001030717" \
          --min_wait 5.0 --max_wait 7.0 --retries 3 --browser "firefox" --headless
          
# Using aliases where supported and exporting to JSONLines
edgar-tool text_search Calabarzon -s "2021-01-01" -o "results.jsonl" -f "all_annual_quarterly_and_current_reports" -r 3 -b "firefox" -h
```

> [!WARNING]
> Combining text search parameters with `entity_id` parameter seems to increase the risk of failed requests on the SEC page due to an apparent bug, we recommend to either avoid doing so (you can specify an empty string for search keywords using `""` and use only entity ID) or setting the number of retries accordingly if you do so.

### Detailed Feature Information

<details>
<summary>Expand to view detailed feature information</summary>

#### Search parameters

Most search parameters from the EDGAR text search page are supported, including:
- `Document word or phrase` (mandatory)
- `Company name, ticker or CIK, or individual's name` (optional)
- `Filing category` (optional)
- `Filed from` and `Filed to` dates (optional)

Currently unsupported search parameters are:
- `Filed date ranges` (since the same behavior can be achieved with `Filed from` and `Filed to` dates)
- `Principal executive offices in` (though it could be added in the future by hardcoding the list of supported values)

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

</details>

## Usage - RSS Feed :card_index:

### What is the RSS feed customized retrieval tool ?

The SEC publish a live feed of filings and this part of the tool lets you monitor particular tickers for new filings, so you can get to-the-minute updates.

The output is a CSV file containing the company and filings' metadata, which can be opened in a spreadsheet program (such as Excel).

### Examples

```bash
# Display help message describing all supported arguments along with their usage, aliases and eventual default values (type q to exit)
edgar-tool rss --help

# Basic one-off usage with export to CSV
edgar-tool rss "GOOG" --output "rss_feed.csv"

# Periodic usage specifying 10 minutes interval duration, with export to JSON
edgar-tool rss "AAPL" "GOOG" "MSFT" --output "rss_feed.json" --every_n_mins 10

# Same example as above, using aliases and exporting to JSONLines (.jsonl)
edgar-tool rss "AAPL" "GOOG" "MSFT" -o "rss_feed.jsonl" -e 10
```

### Detailed Feature Information

<details>
<summary>Expand to view detailed feature information</summary>

#### Companies CIK to Ticker mapping

Since the RSS feed uses CIKs instead of tickers, the tool includes a mapping of CIKs to tickers, which is used to filter the feed by ticker.
This mapping is obtained from the [SEC website](https://www.sec.gov/files/company_tickers.json) and is updated on user request.

#### Periodic retrieval

The RSS feed data returns the last 200 filings and is updated every 10 minutes (which doesn't mean all tickers are updated every 10 minutes).
The tool can fetch the feed either once on-demand, or at regular intervals.

</details>

## Table of Cleaned Financial Data :bank:

There is also a table of data containing most income statements, balance sheets, and cash flow statements for every company traded publicly in the U.S. 

This table is updated intermittently and is [available here for download as a .CSV file](https://edgar.marketinference.com/). You can open this file in Excel, use it as a data source for your own code, or use the simple Python script to access time series for the desired data points. 

The quality of any programmatically produced financial dataset is not going to be as accurate or as complete as a S&P Global or Bloomberg subscription. It should, however, be of comparable accuracy to what you can find on Yahoo Finance and spans a wider time frame.

George Dyer, the former Bellingcat tech fellow who developed the first version of this tool, describes it as: "good enough use in projects such as [Market Inference](https://www.marketinference.com/) and [Graham](https://graham.marketinference.com/info)". 

Please report any inconsistencies in the data to George and he will do his best to refine the existing method.

<details>
<summary>Expand to view the full method</summary>

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

</details>

## Development :octocat:

<details>
<summary>Expand to view information for developers</summary>

This section describes how to install the project to run it from source, for example if you want to build new features.

```bash
# Clone the repository
git clone https://github.com/bellingcat/EDGAR.git

# Change directory to the project folder
cd EDGAR
```

This project uses [Poetry](https://python-poetry.org/docs) for dependency management and packaging.

```bash
# Install poetry if you haven't already
pip install poetry

# Install dependencies
poetry install

# Run the tool
poetry run edgar-tool --help
```
</details>
