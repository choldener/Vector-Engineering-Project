import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
#from figures.mapfigs import create_case_sequence_scatter_mapbox_fig
#from figures.linefigs import line_fig
#from figures.bar_figs import create_bar_fig
from pipeline.call_data import call_full_data
import pandas as pd
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import numpy as np




app = dash.Dash(__name__)
app.title = 'Covid-19 Dashboard'
px.set_mapbox_access_token(open('mapbox_key.txt').read())

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })
    
 
 
 
 
 
 
def create_cases_map_fig(data):
    # fig = go.Figure()
    
    # fig.add_trace(go.Scattermapbox(
        
    #     ))
    # fig.add_trace(go.scattermapbox(
        
    #     ))
    # fig.
    
    
    
    
    # fig_cases = go.Scattermapbox(
    #     name = 'Cases',
    #     lon = data['Long_'],
    #     lat = data['Lat'],
    #     text = data['Cases'],
    #     mode = 'markers',
    #     fillcolor = 'blue',
    #     showlegend = True,
    #     marker = go.scattermapbox.Marker(
    #         size = data['Cases'],
    #         sizeref=2.*max(data['Cases'])/(40.**2),
    #         sizemin=4
    #         color = 'blue',
    #         opacity = 0.75
    #         ),
    #     opacity = 0.75
    #     )
    # fig_sequences = go.Scattermapbox(
    #     name = 'total_sequences',
    #     lon = data['Long_'],
    #     lat = data['Lat'],
    #     text = data['total_sequence'],
    #     mode = 'markers',
    #     fillcolor = 'green',
    #     showlegend = True,
    #     marker = go.scattermapbox.Marker(
    #         size = data['total_sequence'],
    #         sizeref=2.*max(data['total_sequence'])/(40.**2),
    #         sizemin=4
    #         color = 'green',
    #         opacity = 0.75
    #         ),
    #     opacity = 0.75
    #     )
    
    # layout = go.Layout(
    #     height=800,
    #     autosize=True,
    #     mapbox_accesstoken = open('mapbox_key.txt').read(),
    #     mapbox_center={"lat": 37.0902, "lon": -95.7129},
    #     mapbox_style = 'dark'
    #     )
    # figure_array = [fig_cases, fig_sequences]
    # fig = go.Figure(data=figure_array, layout=layout)
    
    
    # fig = px.scatter_mapbox(data, lat = 'Lat', lon = 'Long_', size = 'Cases_scale',
    #                                   #color = , 
    #                                   #color_continuous_scale=px.colors.sequential.Jet, 
    #                                   size_max=100, #zoom=map_zoom, center = dict(lat=center_lat, lon=center_lon),
    #                                   mapbox_style = 'dark', width = 1800, height=1000,
    #                                   #hover_data = ['Confirmed', 'Deaths', 'Recovered', 
    #                                                 #'Case-Fatality_Ratio','current_case']
    #                                                 )
    
    
    with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
        countries = json.load(response)
    fig = px.choropleth_mapbox(data, geojson=countries, locations='iso3', 
                                color = np.log10(data['Cases']), 
                                color_continuous_scale=px.colors.sequential.Jet,
                                opacity=0.5,
                                mapbox_style = 'light', width = 1800, height=1000,
                                hover_name="Country",
                                hover_data = {'total_sequence_scale': False,
                                                'Lat': False,
                                                'Long_': False,
                                                'total_sequence': True,
                                                'Cases': True,
                                                'iso3': False,
                                                },
                        )
    fig.update_layout(coloraxis_colorbar= dict(
        title = 'Cases',
        tickvals = [-1, np.log10(1000),np.log10(10000), np.log10(100000), np.log10(1000000), np.log10(10000000)],
        ticktext = ['0', '1,000', '10,000', '100,000', '1,000,000', '10,000,000']))
    
    fig2 = px.scatter_mapbox(data, lat = 'Lat', lon = 'Long_', size = 'total_sequence_scale',
                                      size_max=70, #zoom=map_zoom, center = dict(lat=center_lat, lon=center_lon),
                                      mapbox_style = 'light', width = 1800, height=1000,
                                      )
    fig2.update_traces(hovertemplate=None, hoverinfo='skip')
    fig.add_trace(
        fig2.data[0]
          )
    
    # with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json') as response:
    #      countries = json.load(response)
    # fig = go.Figure(data = go.Choroplethmapbox(geojson = countries, locations = data['iso3'],
    #                                      z = np.log10(data['Cases']), 
    #                                      colorscale="Viridis",
    #                                      colorbar_title='Cases',
    #                                      marker_opacity=0.5, marker_line_width=1,
    #                                      customdata=[data['Cases'], data['total_sequence'],],
    #                                      #name= data['Country'],
    #                                      text = data['total_sequence'] ,
    #                                      hovertemplate='<br>Total Sequence Count: %{text}<br> %{customdata[0]}'
    #                                      ))
    # fig.update_traces(colorbar=dict(
    #      tickvals = [-1, np.log10(1000),np.log10(10000), np.log10(100000), np.log10(1000000), np.log10(10000000)],
    #      ticktext = ['0', '1,000', '10,000', '100,000', '1,000,000', '10,000,000'])
    #     )
    # fig.update_layout(mapbox_style="carto-positron",
    #                   mapbox_zoom=1, mapbox_center={"lat": 37.0902, "lon": -95.7129}, 
    #                   width = 1800, height=1000
    #     )
    # fig2 = px.scatter_mapbox(data, lat = 'Lat', lon = 'Long_', size = 'total_sequence_scale',)
    # fig2.update_traces(hovertemplate=None, hoverinfo='skip')
    # fig.add_trace(
    #     fig2.data[0]
    #       )
    
    return fig



df = call_full_data()
df = df.loc[df['Date'] == df['Date'].max()]









app.layout = html.Div(children=[

    dcc.Graph(
        id='debug-plot',
        figure=create_cases_map_fig(df)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)