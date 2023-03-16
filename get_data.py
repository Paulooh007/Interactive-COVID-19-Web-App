from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import streamlit as st
import os

CWD = os.path.dirname(os.path.abspath(__file__))


STATES_DAILY_CASES_URL = 'https://github.com/Kamparia/nigeria-covid19-data/raw/master/data/csv/ncdc-covid19-states-daily-cases.csv'
STATES_DAILY_DEATHS_URL = 'https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-deaths.csv'
STATES_DAILY_RECOVERED = 'https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-recovered.csv'
COORD_ULR = 'https://github.com/Kamparia/nigeria-covid19-data/raw/master/data/csv/ncdc-covid19-states.csv'
GEN_UPDATE = 'https://github.com/Kamparia/nigeria-covid19-data/raw/master/data/csv/ncdc-covid19-dailyupdates.csv'
WHO_URL ="https://covid19.who.int/WHO-COVID-19-global-data.csv"

LATEST_NCDC = os.path.join(CWD, "ncdc_latest.csv")


@st.cache
def get_ncdc_data():
    """
    This function uses the latest data from the NCDC website and stores it as a pandas dataframe' 
    """
    data = pd.read_csv(LATEST_NCDC)

    return data


    

## load data function
@st.cache ## caches the output of the function
def get_data():
    '''
    Fuction adds all the needed data to a list to be easily
    accessed by indexing

    0 = states_csv,
    1 = dailyupdates
    2 = states_Daily
    3 = states_daily death
    4 = states_daily_recovery
    5 = who
    '''
    # empty array
    data = []

    ## 0 - ncdc-covid19-states.csv
    states_csv = get_ncdc_data()
    states_csv.columns = ['STATE', 'CONFIRMED','ACTIVE','DISCHARGED', 'DEATHS' ]
    data.append(states_csv)

    ## 1 - ncdc-covid19-dailyupdates.csv
    dailyupdates_csv = pd.read_csv(GEN_UPDATE)
    data.append(dailyupdates_csv)
    

    ## 2 - ncdc-covid19-states-daily-cases.csv
    states_daily_cases_csv = pd.read_csv(STATES_DAILY_CASES_URL)
    data.append(states_daily_cases_csv)

    ## 3 - ncdc-covid19-states-daily-deaths.csv
    states_daily_deaths_csv = pd.read_csv(STATES_DAILY_DEATHS_URL)
    data.append(states_daily_deaths_csv)

    ## 4 - ncdc-covid19-states-daily-recovered.csv
    states_daily_recovered_csv = pd.read_csv(STATES_DAILY_RECOVERED)
    data.append(states_daily_recovered_csv)
    
    ##5 - 'WHO-COVID-19-global-data.csv'
    who = pd.read_csv(WHO_URL)[['Date_reported', 'Country', 'New_cases', 'Cumulative_cases', 
                                'New_deaths', 'Cumulative_deaths']]
    who_daily = who.loc[who['Country'] == 'Nigeria'].reset_index(drop = True)
    who_daily.columns = ['Date_reported', 'Country', 'New_cases', 'Cumulative_cases',
                    'New_deaths', 'Cumulative_deaths']
    data.append(who_daily)
    
    
    return data


if __name__ == "__main__":
    data = get_data()