import pandas as pd # library for data analsysis
import json # library to handle JSON files
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import requests # library to handle requests
import numpy as np
import folium # map rendering library
import streamlit as st
from streamlit_folium import folium_static

from get_data import get_data
#------------------------------------------------

load = get_data()
data_all = load[0]   
data_geo = json.load(open('ncdc-covid19-states.geojson'))


dicts = {"Confirmed":'CONFIRMED',
        "Active": 'ACTIVE',
        "Discharged": 'DISCHARGED',
        "Deaths": 'DEATHS'}

def center():
    address = 'Nigeria'
    geolocator = Nominatim(user_agent="id_explorer")
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude

def threshold(data):
    threshold_scale = np.linspace(data_all[dicts[data]].min(),
                              data_all[dicts[data]].max(),
                              10, dtype=float)
    threshold_scale = threshold_scale.tolist() # change the numpy array to a list
    threshold_scale[-1] = threshold_scale[-1]
    return threshold_scale

def show_maps(data, threshold_scale, color, arg):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_all,
        columns=['STATE',dicts[data]],
        key_on='feature.properties.STATE',
        threshold_scale=threshold_scale,
        fill_color=color, 
        fill_opacity=1, 
        width='60%', height='60%',
        line_opacity=0.9,
        legend_name=dicts[data],
        highlight=True,
        reset=True).add_to(arg)

    folium.LayerControl().add_to(arg)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['STATE',data],
                                                        aliases=['STATE: ', dicts[data]],
                                                        labels=True)) 

    return folium_static(arg)

def show_maps_general(threshold_scale, color, arg):
    maps= folium.Choropleth(
        geo_data = data_geo,
        data = data_all,
        columns=['STATE',dicts["Confirmed"]],
        key_on='feature.properties.STATE',
        threshold_scale=threshold_scale,
        fill_color=color, 
        fill_opacity=1, 
        width='30%', height='30%',
        line_opacity=0.9,
        legend_name=dicts["Confirmed"],
        highlight=True,
        reset=True).add_to(arg)

    folium.LayerControl().add_to(arg)
    maps.geojson.add_child(folium.features.GeoJsonTooltip(fields=['STATE',"Confirmed", 'Deaths', 'Active'],
                                                        aliases=['STATE: ', dicts["Confirmed"],dicts['Deaths'],dicts['Active']],
                                                        labels=True))

    folium_static(arg)



def json_features():
    for idx in range(37):
        data_geo['features'][idx]['properties']['Confirmed'] = int(data_all['CONFIRMED'][idx])
        data_geo['features'][idx]['properties']['Active'] = int(data_all['ACTIVE'][idx])
        data_geo['features'][idx]['properties']['Discharged'] = int(data_all['DISCHARGED'][idx])
        data_geo['features'][idx]['properties']['Deaths'] = float(data_all['DEATHS'][idx])





