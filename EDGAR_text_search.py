# Copyright (C) 2023 George Dyer, Informatism LLC (https://informatism.com/)
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import random
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

###################
### User inputs ###

exact_match = False # select False if you want search to capture combinations of words in search_term

search_term = "synergies" # up to 3 words accepted
annual_quarterly_reports = True # select False if you want all filings
start_date = "2023-11-01"
end_date = "2023-11-02"
headers = {'user-agent': ""} # enter your email address here

driver = webdriver.Chrome() # if you don't have Chrome, you need to select a different browser for the web driver

file_path_output = "" # put the desired directory here for search results e.g. Documents/EDGAR-filings/

###################
### definitions ###

# define now
now = datetime.now()
today = now.strftime("%Y-%m-%d")
last_year = (now - timedelta(days=365)).strftime("%Y-%m-%d")

# define words
words = search_term.split()

# define url building function
def url_build(exact_match = True, annual_quarterly_reports= True, words = None, start_date = None, end_date = None):
    if end_date == None:
        end_date = today
    if start_date == None:
        start_date = last_year

    if words is not None:
        if len(words) == 1:
            word1 = words[0]
        elif len(words) == 2:
            word1, word2 = words
        elif len(words) == 3:
            word1, word2, word3 = words
        else:
            print("Invalid number of words")
        if (len(words)<4 and len(words) > 0):
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

            text_search_url = text_search_url+'&page='
        else:
            text_search_url = None
            print('Invalid Search parameters')
    else:
        text_search_url = None
        print('No Search terms')
    return text_search_url

text_search_url = url_build(exact_match, annual_quarterly_reports, words, start_date, end_date)

# define function for identifying 10,000 + results,=
def get_results_number(text_search_url):
    max_attempts = 4
    rest_time = random.uniform(4, 6)
    num = 1
    for attempt in range(1, max_attempts + 1):
        try:
            driver.get(f'{text_search_url}{num}') 
            time.sleep(rest_time)
            result_page_id_element = driver.find_element(By.ID, 'show-result-count')
            result_page_id_element = result_page_id_element.text
            result_number = int(re.sub(r'\D', '', result_page_id_element))
            return result_number  # If successful, exit the loop and return the result
        except Exception as e:
            print(f'Attempt {attempt} to get results number failed. Error: {e}')
            if attempt < max_attempts:
                print('Retrying...setting longer rest time')
                rest_time = random.uniform(10,14)
                num=num+1
            else:
                print('Max attempts reached. Returning 10_000 as result number.')
                return 10_000

# define function for changing search dates

def change_search_dates(start_date, end_date, book_end = False, shift_by = 180):
    # print('initial start_date')
    # print(start_date)
    # print('initial end date')
    # print(end_date)
    if book_end is False:
        print('shifting end date to last start date')
        end_date = start_date
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    start_date = (end_date - timedelta(days= shift_by)).strftime("%Y-%m-%d")
    end_date = datetime.strftime(end_date, "%Y-%m-%d") 
    # print('new start_date')
    # print(start_date)
    # print('new end date')
    # print(end_date)
    return start_date, end_date

# define function for getting search results and storing as CSV
def get_search_results (text_search_url, result_number):
    # loop through search result pages
    print(f'now searching from {start_date} to {end_date}')
    print('number of results from query:')
    print(result_number)
    full_search_result_table_list =[]  

    page_num = 1
    for page in range(0,100):

        url = f'{text_search_url}{page_num}'
        # print(url)

        ## access search results page
        driver.get(url)
        rest_time = random.uniform(5,10)
        time.sleep(rest_time)

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
            # print("last page!")
            # print("length of page search results")
            # print(len(search_result_table_list))
            search_results =pd.concat(search_result_table_list)
            search_results.sort_values(by='Date',inplace=True)
            search_results.reset_index(inplace=True, drop=True)
            # print(search_results)

            # append results table to list 
            full_search_result_table_list.append(search_results)

            break
        elif result_number <= page_num*100:
            # print("last page!")
            # print("length of page search results")
            # print(len(search_result_table_list))
            search_results =pd.concat(search_result_table_list)
            search_results.sort_values(by='Date',inplace=True)
            search_results.reset_index(inplace=True, drop=True)

            # append results table to list 
            full_search_result_table_list.append(search_results)

            break
        else:
            # print("results found!")
            # print("length of page search results")
            # print(len(search_result_table_list))
            search_results =pd.concat(search_result_table_list)
            search_results.sort_values(by='Date',inplace=True)
            search_results.reset_index(inplace=True, drop=True)

            # append results table to list 
            full_search_result_table_list.append(search_results)

            # increase page_num by 1
            page_num = page_num + 1

            # add a rest
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
        files_to_concatenate.append(f'{file_path_output}{file_name}_{start_date}_{end_date}.csv')

#########################
##### Process Start #####

# define file list 
files_to_concatenate = []

# set result number 
result_number = get_results_number(text_search_url)

if result_number < 10_000:
    # under 10_000 results, no extra work needed, enjoy!
    get_search_results(text_search_url, result_number)
else:
    print('too many results, breaking into parts')
    # we need to break the search up into managable pieces

    book_end = True # book end locks end_date of search period
    start_date_ref = datetime.strptime(start_date, "%Y-%m-%d") # referencing search start date set by user
    shift_by = 180 # this variable represents distance between end_date and start_date

    for i in range(0,100):
        print('Search date segment:')
        print(i)
        if i != 0:
            book_end = False
            start_date, end_date = change_search_dates(start_date, end_date, book_end, shift_by)
            text_search_url = url_build(exact_match, annual_quarterly_reports, words, start_date, end_date)
            result_number = get_results_number(text_search_url)
        else:
            start_date, end_date = change_search_dates(start_date, end_date, book_end)
            text_search_url = url_build(exact_match, annual_quarterly_reports, words, start_date, end_date)
            result_number = get_results_number(text_search_url)
            
        if result_number < 10_000:
            get_search_results(text_search_url, result_number)
            if result_number <= 5_000:
                shift_by = shift_by + 180
        else:
            # try 4 more times to get length right
            print(f'{shift_by} day segments contain too many results, shortening further')
            book_end = True
            shift_by = shift_by/2
            print('shift start_day by')
            print(shift_by)
            for ii in range(0,3):
                if ii  != 0:
                    shift_by = shift_by - 20
                    print('shift start_day by')
                    print(shift_by)
                start_date, end_date = change_search_dates(start_date, end_date, book_end, shift_by)
                text_search_url = url_build(exact_match, annual_quarterly_reports, words, start_date, end_date)
                result_number = get_results_number(text_search_url)
                if result_number < 10_000:
                    print(f'moving start date by {shift_by} contains less than 10,000 results. Getting results')
                    get_search_results(text_search_url, result_number)
                    shift_by = 180
                    break
                elif ii < 3:
                    print(f'moving start date by {shift_by} contains more than 10,000 results, shifting again')
                else:
                    print(f'period of {shift_by} contains more than 10,000 results. Consider new search terms')
                    break
        start_date_compare = datetime.strptime(start_date, "%Y-%m-%d")
        if start_date_compare <= start_date_ref:
            print('new start date has reached initial search start date')
            break

# clean up results #
if len(files_to_concatenate) > 1:

    # Initialize an empty DataFrame
    combined_df = pd.DataFrame()

    # Concatenate files into a single DataFrame
    for file_path in files_to_concatenate:
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # drop duplicates 
    combined_df.drop_duplicates(subset=['Date', 'CIK'], keep='first', inplace=True)

    # sort by year
    combined_df.sort_values(by='Date', ascending=False, inplace=True)

    # reset index 
    combined_df.reset_index(inplace = True, drop=True)

    # Save the combined DataFrame to a new CSV file
    output_file_path = f'{file_path_output}{search_term}_ALL.csv'
    combined_df.to_csv(output_file_path, index=False)
