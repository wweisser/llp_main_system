from dash import Input, Output, html, State
from dash_extensions import EventSource
import gui_utils as gu
import gui_case_management as gcm
import gui_panels as gp
import datetime

def create_note_callback(app):
    @app.callback(
        Output('enter_note_btn', 'n_clicks'),
        Output('note_h1', 'value'),
        Input('enter_note_btn', 'n_clicks'),
        Input('graph_data_store', 'data'),
        Input('state_data_store', 'data'),
        State('note_store', 'value'),
        prevent_initial_call=True
    )
    def enter_note(enter_btn, note_h1):
        if enter_btn:
            return 0,
        else:
            return 0

#send input to backend

#attach input to state

#take note stack form graph update

#merge state and stack notes

    @app.callback(
        Output('note_store', 'data'),
        Input('graph_data_store', 'data'),
        State('note_h1', 'value'),
        prevent_initial_call=True
    )
    def enter_note(enter_btn, note_h1):
        if enter_btn:
            return 0,
        else:
            return 0, 