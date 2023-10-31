import os
import pandas as pd # install pandas
import requests
import json
from bs4 import BeautifulSoup # install lxml beautifulsoup4
import re
from datetime import datetime

####################
### User inpouts ###

# enter your directories / headers here

file_path_input = "Documents/HOMEBREWING/"
file_path_output = "Documents/HOMEBREWING/RSS"
download_dir = f'{file_path_output}/MI_articles/'
headers = {'user-agent': "editor@marketinference.com"}

# enter tickers of interest, or ticker category (country, market cap):

market_cap = 1_000_000_000
tickers = pd.read_csv(f'{file_path_input}/SIMFIN/nasdaq_screener.csv')
tickers = tickers['Symbol'].loc[tickers['Market Cap'] > market_cap]
# print(tickers)

####################
### define today ###

now = datetime.now()
today = now.strftime("%Y-%m-%d")
# print(today)

# url of main XBRL RSS feed

RSS_url = "https://www.sec.gov/Archives/edgar/xbrlrss.all.xml"

# get ticker / CIK table

# Load the JSON file for CIK numbers
file_path = os.path.expanduser(f"{file_path_input}/SIMFIN/company_tickers.json")
with open(file_path) as file:
    data = json.load(file)

tickers_cik = pd.DataFrame.from_dict(data, orient='index')
tickers_cik = tickers_cik[['ticker', 'cik_str']]

# target_forms = [] <link>

### access RSS feed

response = requests.get(url = RSS_url, 
        headers = headers
        )

# Parse the RSS feed
soup = BeautifulSoup(response.content, "xml")
items = soup.find_all('item')

#CIk Pattern
CIK_pattern = "\((\d+)\)"

# Initialize dictionaries to store data
data = {'Company': [], 'Ticker': [], 'CIK': [], 'Description': [], 'Link': [] }

#Loop through items
for item in items:
        title = item.find('title')
        title = title.text

        CIK_match = re.search(CIK_pattern, title)
        CIK = CIK_match.group(1) if CIK_match else None

        # remove CIK from title after extraction
        title = re.sub(r'\([^)]*\)', '', title).strip()

        link = item.find('link')
        link = link.text

        form = item.find('description')
        form = form.text

        # screen for tickers of interest
        # find ticker
        if CIK is not None:
                CIK_screen = int(CIK)
                ticker = tickers_cik['ticker'].loc[tickers_cik['cik_str'] == CIK_screen].values
                if len(ticker) != 0:  # Check if 'ticker' is not an empty Series
                        # ticker_value = ticker[0]  # Assuming you want the first value from 'ticker'
                        ticker = ticker[0]
                        is_in_scope = ticker in tickers.values
                        if is_in_scope:
                                print(f'Adding {ticker} to results')
                               # Append the data to the dictionaries
                                data['Company'].append(title)
                                data['Ticker'].append(ticker)
                                data['CIK'].append(CIK)
                                data['Link'].append(link)
                                data['Description'].append(form)
                
# Create a DataFrame from the dictionaries
daily_RSS_feed = pd.DataFrame(data)

daily_RSS_feed.to_csv(f'{file_path_output}/{today}.csv')

        
