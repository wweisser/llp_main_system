from dash import dcc, html
import plotly.express as px
import numpy as np
import pandas as pd

def create_graph(id, class_name):
    fig = px.scatter(x=None, y=None)
    fig.update_layout(
        margin=dict(l=0, r=10, t=15, b=0),
        xaxis=dict(showgrid=False, showline=False, zeroline=False, linewidth=1, linecolor='#ccebfd'),
        yaxis=dict(showgrid=False, showline=False, zeroline=False,  linewidth=1, linecolor='#ccebfd'),
        paper_bgcolor='#00242b',
        plot_bgcolor='black',
    )
    return(
        html.Div([
            dcc.Graph(figure=fig,
            className='center_graph',
            id=id)
        ], className='center_graph_container')
    )

def create_graph_panel(upper_graph: str, middle_graph: str, lower_graph: str):
    return(
        html.Div([
            create_graph(upper_graph, 'center_graph_container'),
            create_graph(middle_graph, 'center_graph_container'),
            create_graph(lower_graph, 'center_graph_container'),
        ], id='center_graph_panel', className='center_graph_panel')
    )