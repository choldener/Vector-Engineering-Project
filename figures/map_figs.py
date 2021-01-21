import plotly.express as px
import numpy as np 
from pipeline.call_data import call_full_data
from urllib.request import urlopen
import json


def create_case_sequence_scatter_mapbox_fig(relayout_data = None):
    """Creates bar graph with cases represented as color and a bubble representing sequences"""
    #DATA GATHERING
    data = call_full_data()
    data = data.loc[data['Date'] == data['Date'].max()]
    data = data.loc[data['total_sequence'] > 0].sort_values(by=['total_sequence'])
    #geojson
    with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
        countries = json.load(response)
        
    #RELAY DATA
    if relayout_data == None:
            center_lat = 27
            center_lon = 0
            map_zoom = .75
    else:
        center_lat = float(relayout_data['mapbox.center']['lat'])
        center_lon = float(relayout_data['mapbox.center']['lon'])
        map_zoom = float(relayout_data['mapbox.zoom'])
    
    #Colored mapbox creation
    fig = px.choropleth_mapbox(data, geojson=countries, locations='iso3',
                                color = np.log10(data['Cases']),
                                color_continuous_scale=px.colors.sequential.Jet,
                                opacity=0.75,
                                mapbox_style = 'light', width = 900, height=600,
                                hover_name="Country",
                                hover_data = {
                                                'Lat': False,
                                                'Long_': False,
                                                'total_sequence': True,
                                                'Cases': True,
                                                'iso3': False
                                                },
                                zoom=map_zoom, center = dict(lat=center_lat, lon=center_lon,)
    )
    fig.update_layout(coloraxis_colorbar= dict(
        title = 'Cases',
        tickvals = [-1, np.log10(1000),np.log10(10000), np.log10(100000), np.log10(1000000), np.log10(10000000)],
        ticktext = ['0', '1,000', '10,000', '100,000', '1,000,000', '10,000,000']), clickmode='event+select')
    
    #Bubble mapbox creation
    fig2 = px.scatter_mapbox(data, lat = 'Lat', lon = 'Long_', size = 'total_sequence_scale',
                                      size_max=70, zoom=map_zoom, center = dict(lat=center_lat, lon=center_lon),
                                      mapbox_style = 'light', width = 1800, height=1000, opacity=0.5
                                      )
    fig2.update_traces(hovertemplate=None, hoverinfo='skip')
    
    #adding bubble mapbox data to color mapbox
    fig.add_trace(
        fig2.data[0]
          )
    return fig