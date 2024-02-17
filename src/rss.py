from pathlib import Path
from typing import List

import requests
from fake_useragent import UserAgent

RSS_FEED_DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"
RSS_FEED_URL = "https://www.sec.gov/Archives/edgar/xbrlrss.all.xml"
RSS_COMPANY_TICKERS_FILE_PATH = RSS_FEED_DATA_DIRECTORY / "company_tickers.json"
RSS_COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
def daily_rss_feed(tickers: List[str], output_directory: str) -> None:
    # Check if tickers file exists, if not download it
    if RSS_COMPANY_TICKERS_FILE_PATH.exists():
        print("Company tickers file found, skipping download")
    else:
        print("Company tickers file not found, downloading...")
        ua = UserAgent().random
        response = requests.get(RSS_COMPANY_TICKERS_URL,
                                headers={
                                    "user-agent": ua
                                })
        response.raise_for_status()
        with open(RSS_COMPANY_TICKERS_FILE_PATH, "wb") as file:
            file.write(response.content)

#
#
# ####################
# ### User inputs ###
#
# # enter your directories / headers here
#
# file_path_input = "./assets/"  # e.g. "Documents/EDGAR/assets/ – in this directory, you need to place the file downloaded here: https://www.sec.gov/files/company_tickers.json
# file_path_output = "./RSS/"  # e.g. "Documents/EDGAR/RSS/" – this is where the files will be downloaded
# headers = {'user-agent': ""}  # enter (your?) email address
#
# # enter tickers of interest
#
# tickers_list = [
#     #     "PLTR",
#     #     "XOM",
#     #     "AAPL",
#     "CHWY"
# ]
#
#
# # url of main XBRL RSS feed
#
# RSS_url = "https://www.sec.gov/Archives/edgar/xbrlrss.all.xml"
#
# # get ticker / CIK table
# # Load the JSON file for CIK numbers
# file_path = os.path.expanduser(f"{file_path_input}company_tickers.json")
# with open(file_path) as file:
#     data = json.load(file)
#
# tickers_cik = pd.DataFrame.from_dict(data, orient='index')
# tickers_cik = tickers_cik[['ticker', 'cik_str']]
#
# ### access RSS feed
#
# response = requests.get(url=RSS_url,
#                         headers=headers
#                         )
#
# # Parse the RSS feed
# soup = BeautifulSoup(response.content, "xml")
# items = soup.find_all('item')
#
# # CIk Pattern
# CIK_pattern = "\((\d+)\)"
#
# # Initialize dictionaries to store data
# data = {'Company': [], 'Ticker': [], 'CIK': [], 'Description': [], 'Link': []}
#
# # Loop through items
# for item in items:
#     title = item.find('title')
#     title = title.text
#
#     CIK_match = re.search(CIK_pattern, title)
#     CIK = CIK_match.group(1) if CIK_match else None
#
#     # remove CIK from title after extraction
#     title = re.sub(r'\([^)]*\)', '', title).strip()
#
#     link = item.find('link')
#     link = link.text
#
#     form = item.find('description')
#     form = form.text
#
#     # screen for tickers of interest
#     # find ticker
#     if CIK is not None:
#         CIK_screen = int(CIK)
#         ticker = tickers_cik['ticker'].loc[tickers_cik['cik_str'] == CIK_screen].values
#         if len(tickers_list) != 0:  # If ticker list defined by user is not empty, we look for tickers of interest
#             if len(ticker) != 0:
#                 ticker = ticker[0]
#                 if ticker in tickers_list:
#                     print(f'Adding {ticker} to results')
#                     # Append the data to the dictionaries
#                     data['Company'].append(title)
#                     data['Ticker'].append(ticker)
#                     data['CIK'].append(CIK)
#                     data['Link'].append(link)
#                     data['Description'].append(form)
#         else:  # if ticker list is emppty, Append all the data to the dictionaries
#             print(f'Adding {ticker} to results')
#             data['Company'].append(title)
#             data['Ticker'].append(ticker)
#             data['CIK'].append(CIK)
#             data['Link'].append(link)
#             data['Description'].append(form)
#
# # Create a DataFrame from the dictionaries
# # daily_RSS_feed = pd.DataFrame(data)
#
# # daily_RSS_feed.to_csv(f'{file_path_output}/{today}.csv')
#
#
#
#
