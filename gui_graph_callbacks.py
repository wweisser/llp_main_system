from dash import Input, Output, html, State
from dash_extensions import EventSource
import plotly.graph_objects as go
import gui_graphs as gg

def create_graph_callbacks(app, graph: str):
    @app.callback(
        Output(graph, "figure"), 
        Input("graph_data_store", "data"),
        prevent_initial_call=True
        )
    def build_graph(data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
        x=data[0],
        y=data[1],
        mode="lines",
        name=graph
        ))
        fig = gg.center_graph_layout(fig)
        return fig