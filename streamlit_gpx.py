import streamlit as st
from gpxpy import parse
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static


keys=['lat', 'lon', 'elev', 'time']
dict_gpx = {}
for key in keys:
    dict_gpx[key] = []

file = st.file_uploader("Upload waypoinst file: ",type=["gpx"])
if file:
    gpx = parse(file) # type: ignore
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                dict_gpx['lat'].append(point.latitude)
                dict_gpx['lon'].append(point.longitude)
                dict_gpx['elev'].append(point.elevation)
                dict_gpx['time'].append(point.time)
    df_gpx=pd.DataFrame.from_dict(dict_gpx)
    start_lat = df_gpx.loc[0,'lat']
    start_lon = df_gpx.loc[0,'lon']
    end_lat = df_gpx['lat'].iloc[-1]
    end_lon = df_gpx['lon'].iloc[-1]
    m = folium.Map(location=[(start_lat + end_lat)/2, (start_lon + end_lon)/2], zoom_start=16)
    coordinates = [tuple(x) for x in df_gpx[['lat','lon']].to_numpy()]
    folium.PolyLine(coordinates, weight=3).add_to(m)
    folium_static(m)    





#   folium.Marker(     [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
# ).add_to(m)
                

# m = folium.Map(location=[(start_lat + end_lat)/2, (start_lon + end_lon)/2], zoom_start=16)
# st_data = st_folium(m, width=725)


# route_map = folium.Map(
#     location=[latitude,longitude] ,
#     zoom_start=14 ,
#     tiles='CartoDBPositron' )

# coordinates = [tuple(x) for x in 
#  df[['latitude','longitude']].to_numpy()]

# folium.PolyLine(coordinates ,
#  weight=3).add_to(route_map)

# center on Liberty Bell, add marker
# m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
# folium.Marker(
#     [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
# ).add_to(m)



# st.map(df_gpx, size='0.1')