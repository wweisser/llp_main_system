from dash import dcc, html
import plotly.express as px
import numpy as np
import pandas as pd

def update_graph_layout(figure):
    figure.update_layout(
        margin=dict(l=0, r=10, t=15, b=0),
        paper_bgcolor='#00242b',
        plot_bgcolor="#071215",
        xaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            linewidth=0.1,
            gridcolor='#005161',
            tickvals=[0, 20, 40, 60, 80, 100]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            zeroline=False,
            linewidth=0.1,
            gridcolor='#005161',
            tickvals=[0, 10, 25, 50, 100]
        ),
    )
    return figure

def create_graph(id, class_name):
    fig = px.scatter(x=None, y=None)
    fig = update_graph_layout(fig)
    return(
        html.Div([
            dcc.Graph(figure=fig,
            className='center_graph',
            id=id)
        ], className='center_graph_container')
    )

def create_graph_panel(upper_graph: str, middle_graph: str, lower_graph: str,  hidden: bool, store_name: str):
    return(
        html.Div([
            create_graph(upper_graph, 'center_graph_container'),
            create_graph(middle_graph, 'center_graph_container'),
            create_graph(lower_graph, 'center_graph_container'),
            dcc.Store(id=store_name)
        ], className='center_graph_panel', hidden=hidden)
    )

def create_center_panels():
   return(
        html.Div([
            create_graph_panel("ph_graph", "base_lact_graph", "k_gluc_graph", False, 'metabolic_graph_store'),
            # create_graph_panel("gas_flow_fio2_graph", "po2_graph", "pco2_graph", True, 'respiratory_graph_store'),
            # create_graph_panel("flow_graph", "pressure_graph", "hb_hct_graph", True, 'perfusion_graph_store'),
        ]))






# def create_custom_panels(class_name: str):
#        return(
#         html.Div([
#             create_graph('custom_graph_1', 'center_graph_container'),
#             create_graph('custom_graph_2', 'center_graph_container'),
#             create_graph('custom_graph_3', 'center_graph_container'),
#         ], className=class_name, hidden=True))

# def create_graphs():
#    return(
#         html.Div([
#             create_center_panels('center_graph_panel'),
#             create_custom_panels('center_graph_panel'),
#             create_drop_down_menu()
#         ]))
