import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
#My functions
from figures.map_figs import create_case_sequence_scatter_mapbox_fig
from figures.line_figs import create_time_series_country, create_time_series_continent
from figures.bar_figs import create_double_bar_fig, create_case_sequence_ratio_bar_fig
from pipeline.call_data import call_full_data
#############

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#COMMENT THE PREVIOUS CODE IF HOSTING LOCALLY 

app.title = 'Covid-19 Dashboard'
px.set_mapbox_access_token(open('mapbox_key.txt').read())
all_continents = call_full_data()['continent'].unique()
data = call_full_data()


app.layout = html.Div([
    
    #BANNER
    html.Div([
        html.H2("COVID SEQUENCING DASHBOARD"),
        html.Img(src="/assets/covid_image.png")
    ], className="banner"),
    
    html.P("This interactive Dashboard aims to provide visualization for global COVID-19 sequencing coverage. This dashboard is fully interactive and easily customizable. A full writeup can be found at the following link: "),
    dcc.Link('github.com/choldener/Vector-Project', href='https://github.com/choldener/Vector-Project'),
    
    #ROW 1
    html.Div([
        html.Div([ #Column 1
            html.Center(html.Div([html.H2("Case Sequence Map", style={"text-decoration": "underline"})])),
            html.P("The Case Sequence Map displays both the number of cases, represented by country color, and the number of total sequences, represented by the bubble centering on a country. County cases / color is on a log scale for clarity. Countries with 0 sequences are excluded."),
            dcc.Graph(id='map_figure',
                  figure = create_case_sequence_scatter_mapbox_fig()
            )
        ], className="six columns"),
        html.Div([ #Column 2
            dcc.Store(id='memory'),
            html.Center(html.Div([html.H2("Case Sequence Line Chart", style={"text-decoration": "underline"})])),
            html.P("The Case Sequence Line Figure displays both sequences and cases as a line. Datapoints can be filtered by continents, scale can be changed from linear to log, and cases/total sequences can be toggled. Clicking on a country on the Case Sequence Map will pull the historical case and sequence data on the graph."),
            dcc.Graph(id='data_line_fig'),
            dcc.Checklist(
                id="checklist",
                options=[{"label": x, "value": x} 
                         for x in all_continents],
                value=all_continents[:],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.RadioItems(
                id='log_radio_line',
                options=[{'label': 'Log Scale', 'value': 'log'},
                         {'label': 'Linear Scale', 'value': 'linear'}],
                value='linear',
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id="case_sequence_checklist",
                options=[{"label": x, "value": x} 
                         for x in ['Cases', 'total_sequence']],
                value=['total_sequence'],
                labelStyle={'display': 'inline-block'}
            ),
        ],className="six columns")
    ], className="row"),
    
    #ROW 2
    html.Div([ 
        html.Center(html.Div([
            html.Div([html.P("Minimum Number of Sequences", style={"text-decoration": "underline"})]),
            dcc.Input(
                id = 'min_seq',
                placeholder='minimum sequence',
                type='number',
                value=1000
            ),
        ], className="twelve columns"))
        
    ], className='row'),
    
    #ROW 3
    html.Div([
        html.Div([ #Column 1
            html.Center(html.Div([html.H2("Case Sequence Bar Chart", style={"text-decoration": "underline"})])),
            dcc.Graph(id='bar_figure'),

        ], className='six columns'),
        html.Div([ #Column 2 
            html.Center(html.Div([html.H2("Sequence Case Ratio Bar Chart", style={"text-decoration": "underline"})])),
            dcc.Graph(id='case_sequence_ratio_bar'),
        ], className='six columns')  
    ],className="row"),
    
    #ROW 4
    html.Div([ 
        html.Div([
                html.Div([html.P("Set Sequence Number Scale", style={"text-decoration": "underline"})]),
            dcc.RadioItems(
                id='log_radio',
                options=[{'label': 'Log Scale', 'value': 'log'},
                         {'label': 'Linear Scale', 'value': 'linear'}],
                value='log'),
        ], className="three columns"),
        
        html.Div([
            html.Div([html.P("Sort Chart", style={"text-decoration": "underline"})]),
            dcc.RadioItems(
                id='sort_radio_selection',
                options=[{"label": x, "value": x} 
                          for x in ['Cases', 'total_sequence']],
                value='total_sequence',
                labelStyle={'display': 'inline-block'}
            ),
        ], className="three columns"),
    ], className='row'),
    
    #Data Table
    html.Div([
        html.Center(html.H2('Latest Raw Data')),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} 
                     for i in data.columns],
            data=data.loc[data['Date'] == data['Date'].max()].to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="paleturquoise"),
            style_data=dict(backgroundColor="lavender"),
            filter_action="native",
            sort_action="native"
        )
    ])

])


##CALLBACKS##


#LineGraph Callback
@app.callback(
    Output('data_line_fig', 'figure'),
    [Input('map_figure', 'clickData'),
    Input('log_radio_line', 'value'),
    Input("checklist", "value"),
    Input("case_sequence_checklist", "value")])
def update_map_line(ClickData, log_radio_line, checklist,case_sequence_checklist): 
    data = call_full_data()
    try:
        data = data.loc[data['iso3'] == ClickData['points'][0]['location']]
        fig = create_time_series_country(data)     
    except: 
        mask = data.continent.isin(checklist)
        fig = create_time_series_continent(data[mask], case_sequence_checklist)
    fig.update_yaxes(type=log_radio_line)
    fig.update_layout(transition_duration=500)
    try:print(ClickData['points'][0]['location'])
    except: print('unable to print')
    return fig


#Raw Number Bar Callback
@app.callback(
    Output('bar_figure', 'figure'),
    [Input('log_radio', 'value'),
    Input('min_seq', 'value'),
    Input('sort_radio_selection', 'value')])
def update_bar(log_radio, min_seq, sort_radio_selection):
    data = call_full_data()
    data = data.loc[data['Date'] == data['Date'].max()]
    data = data.loc[data['total_sequence'] > min_seq].sort_values(by=sort_radio_selection)
    bar_fig = create_double_bar_fig(data)
    bar_fig.update_xaxes(type=log_radio)
    return bar_fig


#Ratio Bar Callback
@app.callback(
    Output('case_sequence_ratio_bar', 'figure'),
    [Input('min_seq', 'value')])
def update_ratio_bar(min_seq):
    data = call_full_data()
    data = data.loc[data['Date'] == data['Date'].max()]
    data = data.loc[data['total_sequence'] > min_seq].sort_values(by=['case_sequence_ratio'])
    case_sequence_ratio_bar = create_case_sequence_ratio_bar_fig(data)
    return case_sequence_ratio_bar

    
# @app.callback(
#     Output('map_figure', 'figure'))
#     #[Input('log_radio', 'value')],
#     #[State('map_figure', 'relayoutData')])
# #def update_map(log_value, relayout_data):
#    # map_fig = create_case_sequence_scatter_mapbox_fig(relayout_data)
#     #map_fig.update_layout(transition_duration=500)
#     #return map_fig
# def create_map():
#     map_fig = create_case_sequence_scatter_mapbox_fig()
#     map_fig.update_layout(transition_duration=500)
#     return map_fig


if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)