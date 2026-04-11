from dash import Input, Output, no_update
from dash_extensions import EventSource
import plotly.graph_objects as go
import gui_graphs as gg

def create_graph_callback(app, graph: str, store):
    @app.callback(
        Output(graph, "figure"), 
        Input(store, "data"),
        prevent_initial_call=True
    )
    def build_graph(msg):
        if msg['id'] == graph:
            fig = go.Figure()
            try:
                fig.add_trace(go.Scatter(
                x=msg['data']['x'],
                y=msg['data']['y'],
                mode="lines",
                name=graph
                ))
            except Exception as e:
                print('create_graph_callback -> data could not be used for graph\n', e)
            fig = gg.update_graph_layout(fig)
            return fig
        else:
            return no_update

def distibute_graph_input(app, store_I, store_II, store_III):
    @app.callback(
        Output(store_I, "data"),
        Output(store_II, "data"), 
        Output(store_III, "data"), 
        Input("graph_data_store", "data"),
        prevent_initial_call=True
    )
    def dgi(msg):
        if msg and msg['id'] == store_I:
            return msg['data'], no_update, no_update
        elif msg and msg['id'] == store_II:
            return  no_update, msg['data'], no_update
        elif msg and msg['id'] == store_III:
            return  no_update, no_update, msg['data']
        else:
            return no_update
            

def create_graph_callbacks(app, store: str, graph_list: list):
    for graph in graph_list:
        create_graph_callback(app, graph, store)


def create_graph_callback_tree(app):
    update_graph_panel(app, "ph_graph", "base_lact_graph", "k_gluc_graph", 'metabolic_graph_store')
    update_graph_panel(app, "do2_vo2_graph", "po2_graph", "pco2_graph", 'respiratory_graph_store')
    update_graph_panel(app, "flow_graph", "pressure_graph", "hb_hct_graph", 'perfusion_graph_store')