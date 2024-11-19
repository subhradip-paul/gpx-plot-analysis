#%% Header files
import streamlit as st
from gpxpy import parse
from gpxpy.geo import distance

import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import numpy as np
import os

def file_selector(folder_path=r"./gpx_files/Alta Via 2 - Our Way/"):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)


keys=['lat', 'lon', 'elev', 'time', 'speed', 'dist3d']
dict_gpx = {}
for key in keys:
    dict_gpx[key] = []

file = file_selector()
st.write(f'You selected {file}')


if file:
    gpxfile = parse(file)# type: ignore
    sum_lat = 0.
    sum_lon = 0.
    n=0.
    for track in gpxfile.tracks:
        for segment in track.segments:
            for idx, point in enumerate(segment.points):
                dict_gpx['lat'].append(point.latitude)
                dict_gpx['lon'].append(point.longitude)
                dict_gpx['elev'].append(point.elevation)
                dict_gpx['time'].append(point.time)
                dict_gpx['speed'].append(point.speed)
                if idx==0:
                    start_lat=point.latitude
                    start_lon=point.longitude
                    start_elev=point.elevation
                    dict_gpx['dist3d'].append(0.0)
                    dict_gpx['gradient'].append(0.0)
                if idx:
                    dist3d=distance(point.latitude,point.longitude,point.elevation,start_lat,start_lon,start_elev)
                    dict_gpx['dist3d'].append(dist3d)
                    
                sum_lat += point.latitude
                sum_lon += point.longitude
                n +=1                
    st.write(":arrow_up:", track.get_uphill_downhill().uphill)
    # print(track.get_duration()) 
           
    df_gpx=pd.DataFrame.from_dict(dict_gpx)
    
    max_lat = df_gpx['lat'].max
    min_lat = df_gpx['lon'].max
    
    
    m = folium.Map(location=[sum_lat/n, sum_lon/n], min_lat=min_lat, max_lat=max_lat, zoom_start=12)
    folium.TileLayer("HikeBike.HillShading").add_to(m)
    folium.TileLayer(show=False).add_to(m)
    folium.LayerControl().add_to(m)
    coordinates = [tuple(x) for x in df_gpx[['lat','lon']].to_numpy()]
    folium.PolyLine(coordinates, weight=2).add_to(m)
    st_folium(m, width=725)
    fig_elev_time = px.line(
    df_gpx,
    x="time",
    y="elev",
    hover_data=["elev"],
    )
    
    fig_elev_dist = px.line(
    df_gpx,
    x="dist3d",
    y="elev",
    hover_data=["elev"],
    )
    
    
    
    st.plotly_chart(fig_elev_time, use_container_width=True)
    st.plotly_chart(fig_elev_dist, use_container_width=True)