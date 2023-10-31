import os
import pandas as pd
import requests
import random
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

###################
### User inputs ###

file_path_output = "" # enter directory where search results will be downloaded, e.g. "Documents/EDGAR/search results/"

exact_match = True # if True, searches for the entire search term as written, as opposed to individual wors within the search term

search_term = "Sam Bankman Fried" # up to 3 words
annual_quarterly_reports = True
start_date = "2015-01-01"
end_date = "2023-10-23"
headers = {'user-agent': ""} # enter (your?) email address here

# Define driver
driver = webdriver.Chrome() 

# Split the search string by spaces
words = search_term.split()

# Assign the words to variables, handling different cases
if len(words) == 1:
    word1 = words
elif len(words) == 2:
    word1, word2 = words
elif len(words) == 3:
    word1, word2, word3 = words
else:
    print("Invalid number of words")

if exact_match:
    if len(words) == 1:
        text_search_url = f"https://www.sec.gov/edgar/search/#/q=%2522{word1}%2522&dateRange=custom&startdt={start_date}&enddt={end_date}"
    elif len(words) == 2:
        text_search_url = f"https://www.sec.gov/edgar/search/#/q=%2522{word1}%2520{word2}%2522&dateRange=custom&startdt={start_date}&enddt={end_date}"
    elif len(words) == 3:
        text_search_url = f"https://www.sec.gov/edgar/search/#/q=%2522{word1}%2520{word2}%2520{word3}%2522&dateRange=custom&startdt={start_date}&enddt={end_date}"
    else:
        print("Invalid number of words")
else:
    if len(words) == 1:
        text_search_url = f"https://www.sec.gov/edgar/search/#/q=%2520{word1}%2520&dateRange=custom&startdt={start_date}&enddt={end_date}"
    elif len(words) == 2:
        text_search_url = f"https://www.sec.gov/edgar/search/#/q=%2520{word1}%2520{word2}%2520&dateRange=custom&startdt={start_date}&enddt={end_date}"
    elif len(words) == 3:
        text_search_url = f"https://www.sec.gov/edgar/search/#/q=%2520{word1}%2520{word2}%2520{word3}%2520&dateRange=custom&startdt={start_date}&enddt={end_date}"
    else:
        print("Invalid number of words")

if annual_quarterly_reports:
    text_search_url = text_search_url+'&category=form-cat1'

# loop through search result pages
full_search_result_table_list =[]  

page_num = 1
result_page_id = ""
text_search_url = text_search_url+'&page='

for page in range(0,1000):

    url = f'{text_search_url}{page_num}'
    print(url)

    ## access search results page
    driver.get(url)
    rest_time = random.uniform(5,10)
    time.sleep(rest_time)

    # define result page id #  use to identify 10,000 + results, and shorten date scope

    result_page_id_element = driver.find_element(By.ID,'show-result-count')
    result_page_id_element = result_page_id_element.text

    # loop through search results on given page
    search_result_table_list = []

    for elements in driver.find_elements(By.TAG_NAME, "tr"):
        
        # get HTML element text
        html_string = elements.get_attribute('innerHTML')
        # print(html_string)

        # Define the regex patterns for each category
        data_adsh_pattern = r'data-adsh="([^"]+)"'
        file_name_pattern = r'<a [^>]*data-file-name="([^"]+)"[^>]*>([^<]+)</a>'
        entity_names_pattern = r'class="entity-name">(.*?)</td>'
        filing_date_pattern = r'class="filed">(.*?)</td>'
        cik_pattern = r'CIK ([0-9]+)'
        jurisdiction_pattern = r'class="incorporated d-none" nowrap="">(.*?)</td>'
        pob_pattern = r'class="biz-location located d-none" nowrap="">(.*?)</td>'

        # Find data-adsh
        data_adsh_match = re.search(data_adsh_pattern, html_string)
        data_adsh = data_adsh_match.group(1) if data_adsh_match else None

        if data_adsh is not None:

            # Find file_name
            file_name_match = re.search(file_name_pattern, html_string)
            file_name = file_name_match.group(1) if file_name_match else None
            file_name_text = file_name_match.group(2) if file_name_match else None

            # Get jurisdiction
            entity_matches = re.findall(entity_names_pattern, html_string)
            if entity_matches:
                entity = entity_matches[0]
                if "<br>" in entity:
                    split_entity = entity.split('<br>')
                    entity1 = split_entity[0]
                    entity2 = split_entity[1] if len(split_entity) > 1 else None
                else:
                    entity1 = entity
                    entity2 = None
            else:
                entity1 = None
                entity2 = None

            # Find CIK numbers
            cik_matches = re.findall(cik_pattern, html_string)
            if cik_matches:
                cik_numbers = cik_matches
                if len(cik_numbers) > 1:
                    cik_number1 = cik_numbers[0]
                    cik_number2 = cik_numbers[1]
                elif len(cik_numbers) == 0:
                    cik_number1 = None
                    cik_number2 = None
                else:
                    cik_number1 = cik_numbers[0]
                    cik_number2 = None
            else:
                cik_number1 = None
                cik_number2 = None

            # Get filing date
            filing_date_matches = re.findall(filing_date_pattern, html_string)
            if filing_date_matches:
                filing_date = filing_date_matches[0]
            else:
                filing_date = None

            # Get jurisdiction
            jurisdiction_matches = re.findall(jurisdiction_pattern, html_string)
            if jurisdiction_matches:
                jurisdiction = jurisdiction_matches[0]
                if "<br>" in jurisdiction:
                    split_jurisdiction = jurisdiction.split('<br>')
                    jurisdiction1 = split_jurisdiction[0]
                    jurisdiction2 = split_jurisdiction[1] if len(split_jurisdiction) > 1 else None
                else:
                    jurisdiction1 = jurisdiction
                    jurisdiction2 = None
            else:
                jurisdiction1 = None
                jurisdiction2 = None

            # Get pob
            pob_matches = re.findall(pob_pattern, html_string)
            if pob_matches:
                pob = pob_matches[0]
                if "<br>" in pob:
                    split_pob = pob.split('<br>')
                    pob1 = split_pob[0]
                    pob2 = split_pob[1] if len(split_pob) > 1 else None
                else:
                    pob1 = pob
                    pob2 = None
            else:
                pob1 = None
                pob2 = None

            # build filing and file link
            try:
                CIK = cik_number1.strip("0")
            except:
                try:
                    CIK = cik_number2.strip("0")
                except:
                    CIK = None
            
            if CIK is not None:
                asc_num_1 = data_adsh.replace("-", "")
                asc_num_2 = data_adsh
                filing_link = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{asc_num_1}/{asc_num_2}-index.html"
                file_link = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{asc_num_1}/{file_name}"
            else:
                filing_link = None

            # define table
            search_result_table = pd.DataFrame(columns = ['Date', 'Jurisdiction', 'Place of Business', 'Entity', 'Entity Alt','CIK', 'CIK Alt', 'Form', "File Link","Filing Link"], 
                                            data = [[filing_date, jurisdiction1, pob1, entity1, entity2, cik_number1, cik_number2, file_name_text, file_link, filing_link]])
            
            if len(search_result_table) != 0:
                search_result_table_list.append(search_result_table)

    # if there are search results, we concatenate and move to next search results page after random rest. 
    # if not, we break loop and save what we got.

    if len(search_result_table_list) == 0:
        print("no search results on page")
        break
    elif len(search_result_table_list) != 100:
        print("last page!")
        print("length of list of result tables")
        print(len(search_result_table_list))
        search_results =pd.concat(search_result_table_list)
        search_results.sort_values(by='Date',inplace=True)
        search_results.reset_index(inplace=True, drop=True)
        break
    else:
        print("results found!")
        print("length of list of result tables")
        print(len(search_result_table_list))
        search_results =pd.concat(search_result_table_list)
        search_results.sort_values(by='Date',inplace=True)
        search_results.reset_index(inplace=True, drop=True)
     
        page_num = page_num + 1

        full_search_result_table_list.append(search_results)
        
        rest_time = random.uniform(0.1,2.5)
        time.sleep(rest_time)

# outside of loop, we concatenate the individual page result tables into final table

if len(full_search_result_table_list) == 0:
    print('There were no results for this query')
else:
    full_search_results =pd.concat(full_search_result_table_list)
    full_search_results.sort_values(by='Date',inplace=True)
    full_search_results.drop_duplicates(subset=['Filing Link'],inplace=True)
    full_search_results.reset_index(inplace=True, drop=True)

    file_name = search_term.replace(" ", "_")

    full_search_results.to_csv(f'{file_path_output}{file_name}_{start_date}_{end_date}.csv')


