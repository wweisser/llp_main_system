from dash import Input, Output, html, State
from dash_extensions import EventSource
import gui_utils as gu
import gui_case_management as gcm
import gui_panels as gp

def create_graph_callback(app, graph_id: str, parameter_I:str, legend_I:str, parameter_II: str, legend_II:str):
      @app.callback(
        Output(graph_id, 'children'),
        Input('inbox', 'data'),
        prevent_initial_call=True,
    )

