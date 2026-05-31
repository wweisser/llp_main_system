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

    
    # modify cm modal

def state_to_button(app, parameter, btn):
    @app.callback(
        Output(btn, 'children'),
        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def process(msg):
        try:
            if isinstance(msg, dict) and msg['msg_type'] == 'system' and msg['id'] == 'state':
                data = msg['data']
                val = data[parameter]['val']
                if not isinstance(val, str):
                    val = str(val)
                return val
            else:
                return ""
        except Exception as e:
            print(f'parameter_to_button -> {parameter} could not be linked to a button')
            return ""

def heartbeat_to_button(app, parameter, btn_I, btn_II):
        @app.callback(
        Output(btn_I, 'children'),
        Output(btn_II, 'children'),
        Input('heartbeat_data_store', 'data'),
        State('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def process(msg, state):
        try:
            if isinstance(msg, dict) and msg['data']['heartbeat_time']:
                ct = msg['data']['heartbeat_time']
            else:
                ct = "---"
            if state and isinstance(state, dict) and state['data']['system']['start_time'] != 0:
                st = state['data']['system']['start_time']
                pt = datetime.now() - datetime.strptime(st, "%Y.%m.%d %H:%M:%S")
            else:
                pt = "---"
            return ct, pt
        except Exception as e:
            print(f'heartbeat_to_button -> error during heartbeat processing: {e}')
            return "", ""


def case_data_to_button(app, pre_text, parameter, btn):
    @app.callback(
        Output(btn, 'children'),
        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def process(msg):
        try:
            if isinstance(msg, dict) and msg['msg_type'] == 'state':
                data = msg['data']
                val = data['system'][parameter]
                if not isinstance(val, str):
                    val = str(val)
                string = f'{pre_text} {val}'    
                return string
            else:
                return f'{pre_text}'
        except Exception as e:
            print(f'system_to_button -> {parameter} could not be linked to a button {val['system'][parameter]}\n')
            return ""

def state_to_gui(app):
    print(f'state_to_gui -> gui updated')
    return(html.Div([
        heartbeat_to_button(app, 'Perfusion: ', 'perfusion_time', 'perfuison_time'),
        heartbeat_to_button(app, 'Clocktime:', 'clock_time', 'clock_time'),

        case_data_to_button(app, 'Case ID:    ', 'case_number', 'case_id'),
        case_data_to_button(app, 'Start: ', 'start_time', 'start_time'),
        case_data_to_button(app, 'Mode: ', 'perfusion_mode', 'perfusion_mode'),

        state_to_button(app, 'art_flow', 'art_flow'),
        state_to_button(app, 'art_pressure', 'art_pressure'),
        state_to_button(app, 'art_temp', 'art_temp'),
        state_to_button(app, 'ven_flow', 'ven_flow'),
        state_to_button(app, 'ven_pressure', 'ven_pressure'),
        state_to_button(app, 'ven_temp', 'ven_temp'),
        state_to_button(app, 'art_ph', 'art_ph'),
        state_to_button(app, 'art_pco2', 'art_pco2'),
        state_to_button(app, 'art_po2', 'art_po2'),
        state_to_button(app, 'hco3', 'hco3'),
        state_to_button(app, 'base', 'base'),
        state_to_button(app, 'cso2', 'cso2'),
        # state_to_button(app, 'na', 'btn'),
        state_to_button(app, 'k', 'k'),
        # state_to_button(app, 'ca', 'btn'),
        # state_to_button(app, 'cl', 'btn'),
        state_to_button(app, 'vo2', 'vo2'),
        state_to_button(app, 'do2', 'do2'),
        state_to_button(app, 'ven_ph', 'ven_ph'),
        state_to_button(app, 'ven_pco2', 'ven_pco2'),
        state_to_button(app, 'ven_po2', 'ven_po2'),
        # state_to_button(app, 'hct', 'btn'),
        # state_to_button(app, 'hb', 'btn'),
        # state_to_button(app, 'lactate', 'btn'),
        # state_to_button(app, 'glucose', 'btn'),
        # state_to_button(app, 'system_volume', 'btn'),
        # parameter_to_button(app, 'filter_flow', 'btn'),
        # parameter_to_button(app, 'substitude_flow', 'btn'),
    ]))