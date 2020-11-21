import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from get_data import get_data


load = get_data()
states = load[0]

states_daily_cases_csv = load[2]
states_daily_deaths_csv = load[3]
states_daily_recovered_csv = load[4]






def summary(state):

    df = states.loc[states['STATE'] == state].reset_index(drop = True)

    confirmed = df['CONFIRMED'][0]
    active = df['ACTIVE'][0]
    discharged = df['DISCHARGED'][0]
    deaths = df['DEATHS'][0]

    st.subheader(f"{state}")
    st.markdown(
                    """
                    Total Confirmed Cases | Total Active Cases | Total Discharged | Total Deaths
                    ----------------|--------------|------------|----------
                    {0}             | {1}          | {2}        | {3} 
                    """.format(confirmed, active, discharged, deaths )
            )
    st.text("")

    
    data = go.Pie(
                labels = ['CONFIRMED', 'ACTIVE', 'RECOVERED','DEATHS'], 
                values = [confirmed, active, discharged, deaths], 
                textinfo='value', 
                textfont=dict(size=20),
                marker=dict(colors =  ['#2d47f9','#ffd700' ,'#228b22','#ff0000' ], 
                    line=dict(color='#FFF', width=1)
                ), hole = .3)
    fig = go.Figure(data = [data])
    fig.update_layout(margin=dict(l=0, r=0, t=2, b=2, pad=2))
    st.plotly_chart(fig)



## total cases overtime charts
def total_cases_overtime(state):
    st.subheader("Total Confirmed Cases:")
    st.write("Total number of confirmed cases over time.")
    df = states_daily_cases_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['Date']), y = df[state], name = state)
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)


## total deaths overtime charts
def total_deaths_overtime(state):
    st.subheader("Total Deaths:")
    st.write("Total number of recorded deaths over time.")
    df = states_daily_deaths_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['Date']), y = df[state], name = state)
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(239, 85, 58)')
    st.plotly_chart(fig)


## total discharged overtime charts
def total_discharged_overtime(state):
    st.subheader("Total Discharged:")
    st.write("Total number of discharged cases over time.")
    df = states_daily_recovered_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['Date']), y = df[state], name = state)
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(89, 205, 150)')
    st.plotly_chart(fig)

