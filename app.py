import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from PIL import Image

import time
import json

from get_data import get_data
from maps import show_maps, threshold, center, json_features, show_maps_general

import folium # map rendering library
from streamlit_folium import folium_static

from states import summary, total_deaths_overtime, total_cases_overtime, total_discharged_overtime

######################################################################################
# MAP VARIABLES FOR PLOTTING
json_features()
centers = center() 

# map_active = folium.Map(tiles='OpenStreetMap', location=[centers[0], centers[1]], zoom_start=6.4)
map_discharged = folium.Map(tiles='OpenStreetMap', location=[centers[0], centers[1]], zoom_start=6.4)
map_deaths = folium.Map(tiles='OpenStreetMap', location=[centers[0], centers[1]], zoom_start=6.4)
map_confirmed = folium.Map(tiles='OpenStreetMap', location=[centers[0], centers[1]], zoom_start=6.4)
map_general = folium.Map(tiles='OpenStreetMap', location=[centers[0], centers[1]], zoom_start=6.4)


def main():
    img = Image.open("covidimg3.jpg")
    st.title("Nigeria COVID-19 Data Explorer")
    st.image(img)
    st.write("Get all information about the current COVID-19 situation in Nigeria.")
    
    #############################################################################
    # LOAD DATASETS

    load = get_data()
    who_data = load[5]
    general_data = load[1]
    states = load[0]


    st.subheader("General Overview/Summary:")
    


    ## Navigation side bar
    nav = st.sidebar.radio('NAVIGATION', ['General Overview', 'Analysis by State'])
    if nav == 'General Overview':
        
            
        sidebar_visual_option = st.sidebar.selectbox(
            'Visual Type:', ('Charts', 'Tables', 'Maps')
        )

    else :
        
        state = st.sidebar.selectbox("Select States: ", states['STATE'])
        st.write(f"Summary of COVID-19 cases in {state}.")

        summary(state)

        total_cases_overtime(state)
        total_discharged_overtime(state)
        total_deaths_overtime(state)

    
    if nav == 'General Overview' and sidebar_visual_option == 'Charts':
        ###########################  HEADER  #################################

        
        df = states
        cases_no = df['CONFIRMED'].sum()
        active_no = df['ACTIVE'].sum()
        deaths_no = df['DEATHS'].sum()
        recovered_no = df['DISCHARGED'].sum()

        st.markdown(
                """
                Total Confirmed Cases | Total Active Cases | Total Discharged | Total Deaths
                ----------------|--------------|------------|----------
                {0}             | {1}          | {2}        | {3} 
                """.format(cases_no, active_no, recovered_no, deaths_no)
        )
        st.text("")
        st.text("")
        st.text("")

        ###########################  Pie Chart  #################################
        
        data = go.Pie(
            labels = ['CONFIRMED', 'ACTIVE', 'RECOVERED','DEATHS'], 
            values = [cases_no, active_no, recovered_no, deaths_no], 
            textinfo='value', 
            textfont=dict(size=20),
            marker=dict(colors =  ['#2d47f9','#ffd700' ,'#228b22','#ff0000' ], 
                line=dict(color='#FFF', width=1)
            ), hole = .3)
        fig = go.Figure(data = [data])
        fig.update_layout(margin=dict(l=0, r=0, t=2, b=2, pad=2))
        st.plotly_chart(fig)
        st.text("")
        st.text("")
        st.text("")


        ###########################  General Maps  #################################
        st.subheader("Reference Map of All Affected States")
        st.write("Mouseover(or Tap on) any state for breakdown of cases")


        show_maps_general(threshold('Confirmed'), 'YlOrBr', arg = map_general)
        st.text("")
        st.text("")
        st.text("")

        ###########################  Daily Trends  #################################
        st.subheader("Daily Trend of Confirmed Cases")
        st.write("Mouseover(or Tap on) chart to see values")
        

        fig = go.Figure(data=[go.Bar(
        x=who_data['Date_reported'],
        y=who_data['New_cases']
        )])
        fig.update_layout(title_text='Daily Confimed Cases',
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=700,height=400)
        st.plotly_chart(fig)
        st.text("")
        st.text("")
        st.text("")

        

        st.subheader("Daily Trend of Death Cases")
        st.write("Mouseover(or Tap on) chart to see values")

        fig = go.Figure(data=[go.Bar(
            x=who_data['Date_reported'],
            y=who_data['New_deaths'],
            marker_color='crimson' # marker color can be a single color value or an iterable
        )])
        fig.update_layout(title_text='Daily Death Cases',
                            legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),
                            width=700,height=400)
        st.plotly_chart(fig)

        st.subheader("Cummulative Number of Cases.")
        st.write("Mouseover(or Tap on) chart to see values")

        df = general_data.sort_values(by='DATE', ascending=False)
        confirmed = go.Bar(
            x = pd.to_datetime(df['DATE']),
            y = df['ACTIVE CASES'],
            name = 'ACTIVE')
        recovered = go.Bar(
            x = pd.to_datetime(df['DATE']),
            y = df['RECOVERED'],
            name = 'RECOVERED')
        deaths = go.Bar(
            x = pd.to_datetime(df['DATE']),
            y = df['DEATHS'],
            name = 'DEATHS')

        layout = go.Layout(barmode='stack')
        fig = go.Figure(data=[confirmed, deaths, recovered], layout=layout)
        fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0),width=700,height=400)
        st.plotly_chart(fig)


    if nav == 'General Overview' and sidebar_visual_option == 'Maps': 

        ####################### MAPS ###################################

        st.subheader("Number of Confirmed Cases:")
        st.write("Mouseover(or Tap on) any state to see numbers")
        show_maps('Confirmed', threshold('Confirmed'), 'Blues', arg = map_confirmed)
        st.text("")
        st.text("")
        st.text("")
        st.subheader("Number of Discharged/Recovered Cases:")
        st.write("Mouseover(or Tap on) any state to see numbers")
        show_maps('Discharged', threshold('Discharged'), 'Greens', arg = map_discharged)
        st.text("")
        st.text("")
        st.text("")
        st.subheader("Number of Deaths Cases:")
        st.write("Mouseover(or Tap on) any state to see numbers")
        show_maps('Deaths', threshold('Deaths'), 'Reds', arg = map_deaths)

    if nav == 'General Overview' and sidebar_visual_option == 'Tables':
        st.subheader("Breakdown of COVID-19 cases by States.")

        st.table(states[["STATE", "CONFIRMED", "DEATHS", "DISCHARGED", "ACTIVE"]])



    st.subheader("About this App:")
    st.markdown(
        """
        
        **Data Scientist / Developer:** [Paul Okewunmi](https://linkedin.com/in/paul-okewunmi-a24526171). 

        **Data Sources:** 
         - [Nigeria Centre for Disease Control (NCDC)](https://covid19.ncdc.gov.ng/).
           - [Code to Scape data](https://gist.github.com/Paulooh007/d591fc4d8d47459c5f4723c003c27e00#file-get_ncdc_data-py)
          
         - [WHO Covid 19 Dashboard.](https://covid19.who.int/WHO-COVID-19-global-table-data.csv)
           - [downloadable csv](https://covid19.who.int/WHO-COVID-19-global-table-data.csv)

         - [COVID-19 States Geojson](https://github.com/Paulooh007/Interactive-COVID-19-Web-App/blob/main/ncdc-covid19-states.geojson)
        """
    )

    
    










if __name__ == "__main__":
    main()