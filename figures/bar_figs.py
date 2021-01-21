import plotly.express as px
import plotly.graph_objects as go


def create_double_bar_fig(data):
    """Creates bar graph with two bars for each Country"""
    fig = go.Figure(data = [
        go.Bar(name='Sequences', y=data['Country'], x=data['total_sequence'], orientation='h'),
        go.Bar(name='Cases', y=data['Country'], x=data['Cases'], orientation='h')
    ])
    fig.update_layout(barmode='group', height = 900, width = 900, margin={'t': 0})
    fig.update_yaxes(tickmode='linear', title = 'Countries')
    fig.update_xaxes(title='Total Amount of Sequences or Cases')
    return fig


def create_case_sequence_ratio_bar_fig(data):
    """Creates a bar graph with my sequence population normalization applied"""
    fig = go.Figure(data = [
        go.Bar(name='Sequences', y=data['Country'], x=data['case_sequence_ratio'], orientation='h'),
    ])
    fig.update_layout(height = 900, width = 900, margin={'t': 0})
    fig.update_yaxes(tickmode='linear', title = 'Countries')
    fig.update_xaxes(title='Sequences/Cases Ratio')
    return fig

