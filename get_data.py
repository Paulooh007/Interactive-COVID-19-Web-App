from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import streamlit as st


STATES_DAILY_CASES_URL = 'https://github.com/Kamparia/nigeria-covid19-data/raw/master/data/csv/ncdc-covid19-states-daily-cases.csv'
STATES_DAILY_DEATHS_URL = 'https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-deaths.csv'
STATES_DAILY_RECOVERED = 'https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-recovered.csv'
COORD_ULR = 'https://github.com/Kamparia/nigeria-covid19-data/raw/master/data/csv/ncdc-covid19-states.csv'
GEN_UPDATE = 'https://github.com/Kamparia/nigeria-covid19-data/raw/master/data/csv/ncdc-covid19-dailyupdates.csv'
WHO_URL ="https://covid19.who.int/WHO-COVID-19-global-data.csv"




@st.cache
def get_ncdc_data():
    """
      This function extracts data from the NCDC website and stores it as a pandas dataframe' 
    """
    PAGE_URL = "https://covid19.ncdc.gov.ng/"
    
    
    # Response Data
    response_data = requests.get(PAGE_URL).text

    # Initializing the BeautifulSoup package and the specifying the parser
    soup = BeautifulSoup(response_data, 'lxml')
    content_table = soup.find("table", id="custom1")

    # Extracting the Table header names 
    table_headers = content_table.thead.findAll("tr")
    for k in range(len(table_headers)):
        data = table_headers[k].find_all("th")
        column_names = [j.string.strip() for j in data]

    # Extracting the data in the Table's body (values)
    table_data = content_table.tbody.findAll('tr')
    values = []
    keys = []
    data_dict = {}
    for k in range(len(table_data)):
        key = table_data[k].find_all("td")[0].string.strip()
        value = [j.string.strip() for j in table_data[k].find_all("td")]
        keys.append(key)
        values.append(value)
        data_dict[key] = value
        
    #Convert dictionary to dataframe 
    data = pd.DataFrame(data_dict).T
    data.columns = ['state', 'confirmed', 'active', 'recovered', 'deaths']
    data = data.sort_values(by = 'state', ignore_index=True)
    data = data.reset_index(drop=True)
    
    #Removing the commas ( , ) between the numbers e.g 6,239
    data['confirmed'] = data['confirmed'].apply(lambda x: int(re.sub("[^0-9]", "", x)) )
    data['active'] = data['active'].apply(lambda x: int(re.sub("[^0-9]", "", x)) )
    data['recovered'] = data['recovered'].apply(lambda x: int(re.sub("[^0-9]", "", x)) )
    data['deaths'] = data['deaths'].apply(lambda x: int(re.sub("[^0-9]", "", x)) )
    
    #join States coordinate for map plot

    return data