from dash import dcc, html
import plotly.express as px
import numpy as np
import pandas as pd

def center_graph_layout(fig):
    fig.update_layout(
        margin=dict(l=0, r=10, t=15, b=0),
        xaxis=dict(showgrid=False, showline=False, zeroline=False, linewidth=1, linecolor='#ccebfd'),
        yaxis=dict(showgrid=False, showline=False, zeroline=False,  linewidth=1, linecolor='#ccebfd'),
        paper_bgcolor='#00242b',
        plot_bgcolor='black',
    )
    return fig

def create_graph(id, class_name):
    fig = px.scatter(x=None, y=None)
    fig = center_graph_layout(fig)
    return(
        html.Div([
            dcc.Graph(figure=fig,
            className='center_graph',
            id=id)
        ], className='center_graph_container')
    )

def create_graph_panel(upper_graph: str, middle_graph: str, lower_graph: str,  hidden: bool, class_name: str):
    return(
        html.Div([
            create_graph(upper_graph, 'center_graph_container'),
            create_graph(middle_graph, 'center_graph_container'),
            create_graph(lower_graph, 'center_graph_container'),
        ], id='center_graph_panel', className=class_name, hidden=hidden)
    )

def create_center_panels(class_name: str):
   return(
        html.Div([
            create_graph_panel("ha_pv_flow_graph", "ha_pv_temp_graph", "hb_hct_graph", False, 'center_graph_panel'),
            # create_graph_panel("ha_pv_ph_graph", "base_lactate_graph", "k_glucose_graph", True, 'center_graph_panel'),
            # create_graph_panel("vo2_do2_flow_graph", "art_ven_po2_graph", "art_ven_pco2_graph", True, 'center_graph_panel'),
        ]))

def create_dropdown(options: dict, id: str, name: 'str'):
    layout = html.Div([
                html.Div(children=name),
                dcc.Dropdown(options=options, value='Select', id=id, multi=True, closeOnSelect=False, searchable=True, className='ha'),
            ])
    # @callback(
    #     Output('close-on-select-output', 'children'),
    #     Input('close-on-select-dropdown', 'value')
    # )
    # def update_output(value):
    #     return f'You have selected {value}'
    return layout

def create_drop_down_menu():
    return(html.Div([
        create_graph('plot_graph', "class_name"),
        create_dropdown({'dummy': 'dummy'}, 'case_number_drop_down', 'case Number'),
        create_dropdown({'dummy': 'dummy'}, 'chart_1', 'Graph 1'),
        create_dropdown({'dummy': 'dummy'}, 'chart_2', 'Graph 2'),
        create_dropdown({'dummy': 'dummy'}, 'chart_3', 'Graph 3'),
        create_dropdown({'dummy': 'dummy'}, 'chart_4', 'Graph 5'),
        create_dropdown({'dummy': 'dummy'}, 'data_export', 'Export to Excel'),
    ], id='drop_down_menu', className='hide'))


def create_custom_panels(class_name: str):
       return(
        html.Div([
            create_graph('custom_graph_1', 'center_graph_container'),
            create_graph('custom_graph_2', 'center_graph_container'),
            create_graph('custom_graph_3', 'center_graph_container'),
        ], className=class_name, hidden=True))

def create_graphs():
   return(
        html.Div([
            create_center_panels('center_graph_panel'),
            create_custom_panels('center_graph_panel'),
            create_drop_down_menu()
        ]))
