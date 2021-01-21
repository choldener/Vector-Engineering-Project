import plotly.express as px 


def create_time_series_country(data):
    """Creates a line graph when clicking a country"""
    fig = px.line(data, x = 'Date', y = ['total_sequence', 'Cases'], title='Country Selected')
    fig.update_xaxes(showspikes= True, spikedash="dot")
    fig.update_layout(hovermode='x', spikedistance=1000, plot_bgcolor="#FFFFFF", width = 900)
    return fig


def create_time_series_continent(data, case_sequence_checklist):
    """Creates a line graph before a country is clicked"""
    fig = px.line(data, x = 'Date', y = case_sequence_checklist, color = 'Country', render_mode='webgl')
    fig.update_xaxes(showspikes= True, spikedash="dot")
    fig.update_layout(hovermode='x', spikedistance=1000, plot_bgcolor="#FFFFFF", width = 900)
    return fig