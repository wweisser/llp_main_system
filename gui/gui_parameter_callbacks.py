from dash import Input, Output, html, State
from dash_extensions import EventSource
import gui_utils as gu
import gui_case_management as gcm
import gui_panels as gp
import datetime

def tabbar_callbacks(app):
    @app.callback(
        Output('cntrl_cm_upper', 'children'),
        Input('inbox', 'data'),
        prevent_initial_call=True,
    )
    def update_case_id(msg):
        if isinstance(msg, dict) and msg['msg_type'] == 'system' and msg['id'] == 'state':
            return msg['system']['case_number']
        else: 
            return ""
    
    @app.callback(
        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def update_perfsuion_state(perfusion_time, perfusion_mode):
        clock_time = datetime.time()
        return perfusion_time, perfusion_mode, clock_time
    
    @app.callback(

    )
    def update_save_mode(save_interval, last_save):
        return save_interval, last_save
    
    # modify cm modal

def parameter_to_button(app, parameter, btn):
    @app.callback(
        Output(btn, 'children'),
        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def process(msg):
        if isinstance(msg, dict) and msg['msg_type'] == 'system' and msg['id'] == 'state':
            data = msg['data']
            val = data[parameter]['val']
            if not isinstance(val, str):
                val = str(val)
            return val
        else:
            return ""
    
def system_to_button(app, pre_text, parameter, btn):
    @app.callback(
        Output(btn, 'children'),
        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def process(msg):
        if isinstance(msg, dict) and msg['msg_type'] == 'system' and msg['id'] == 'state':
            data = msg['data']
            val = data['system'][parameter]
            if not isinstance(val, str):
                val = str(val)
            string = f'{pre_text} {val}'    
            return string
        else:
            return f'{pre_text}'  

def state_to_gui(app):
    return(html.Div([
        system_to_button(app, 'Case ID:    ', 'case_number', 'case_id'),
        system_to_button(app, 'Start of Perfusion:     ', 'start_time', 'start_time'),
        system_to_button(app, 'Perfusion: ', 'perfusion_time', 'perfuison_time'),
        system_to_button(app, 'Clocktime:', 'clock_time', 'clock_time'),
        system_to_button(app, 'Mode: ', 'perfusion_mode', 'perfusion_mode'),

        parameter_to_button(app, 'art_flow', 'art_flow'),
        parameter_to_button(app, 'art_pressure', 'art_pressure'),
        parameter_to_button(app, 'art_temp', 'art_temp'),
        parameter_to_button(app, 'ven_flow', 'ven_flow'),
        parameter_to_button(app, 'ven_pressure', 'ven_pressure'),
        parameter_to_button(app, 'ven_temp', 'ven_temp'),
        parameter_to_button(app, 'art_ph', 'art_ph'),
        parameter_to_button(app, 'art_pco2', 'art_pco2'),
        parameter_to_button(app, 'art_po2', 'art_po2'),
        # parameter_to_button(app, 'hco3', 'hco3'),
        parameter_to_button(app, 'base', 'base'),
        parameter_to_button(app, 'cso2', 'cso2'),
        # parameter_to_button(app, 'na', 'btn'),
        parameter_to_button(app, 'k', 'k'),
        # parameter_to_button(app, 'ca', 'btn'),
        # parameter_to_button(app, 'cl', 'btn'),
        parameter_to_button(app, 'vo2', 'vo2'),
        parameter_to_button(app, 'do2', 'do2'),
        parameter_to_button(app, 'ven_ph', 'ven_ph'),
        parameter_to_button(app, 'ven_pco2', 'ven_pco2'),
        parameter_to_button(app, 'ven_po2', 'ven_po2'),
        # parameter_to_button(app, 'hct', 'btn'),
        # parameter_to_button(app, 'hb', 'btn'),
        # parameter_to_button(app, 'lactate', 'btn'),
        # parameter_to_button(app, 'glucose', 'btn'),
        # parameter_to_button(app, 'system_volume', 'btn'),
        # parameter_to_button(app, 'filter_flow', 'btn'),
        # parameter_to_button(app, 'substitude_flow', 'btn'),
    ]))