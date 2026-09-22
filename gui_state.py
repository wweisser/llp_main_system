from dash import html, dcc, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
import gui_utils as gu
from datetime import datetime
import time


### Frage: wie muss das zusammenspiel zwischen beat in heartbeat_ds und state_ds gelöst werden, um ein sinnvollen hadshake zu erzeugen?

def create_msg_distribution():
    print('distribution stores created')
    return(html.Div([
        dcc.Store(id='postbox', storage_type='memory'),
        dcc.Store(id='inbox', storage_type='memory'),
        dcc.Store(id='download_store', storage_type='session'),

        dcc.Store(id='heatbeat_ds', storage_type='memory'),
        dcc.Store(id='state_ds', storage_type='memory'),

        dcc.Store(id='metabolic_graph_store', storage_type='memory'),
        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory'),
        dcc.Store(id='note_data_store', storage_type='memory'),
        dcc.Store(id='system_data_store', storage_type='memory'),
    ]))

def beat(handshake:bool, last_heartbeat:int, status:str = None, error_state:str = None):
    beat_msg = {
        'handshake': handshake,
        'last_heartbeat': last_heartbeat,
        'time': int(time.time()),
        'status': status,
        'error_state': error_state,
    }
    return gu.create_postbox_item('system', 'f_heartbeat', beat_msg)

def create_heartbeat_intervall(hb_rythm:int = None):
    if not hb_rythm:
        hb_rythm = 1000
    intervall = (html.Div([
        dcc.Interval(id='heartbeat_rythm', interval=hb_rythm)
    ]))
    return intervall

def create_heartbeat_callback(app):
    """creates funktion, that sends heartbeatitem to the postbox in set heartbeat_interval"""
    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Output('state_ds', 'data', allow_duplicate=True),
        Input('heartbeat_rythm', 'n_intervals'),
        State('state_ds', 'data'),
        # prevent_initial_call=True
    )
    def f_heartbeat(n_intervals, gui_state):
        if gui_state:
            beat_msg = beat(gui_state['handshake'], gui_state['time'])
        else:
            beat_msg = beat(False, int(time.time()), status='request_handshake')
            print(f'create_heartbeat_callback -> initial beat was created')
        bltn = gu.dispatch(msg_type='system', id='beat', data=beat_msg)
        return bltn, beat_msg

    @app.callback(
        Output('clock_time', 'children'),
        Output('state_ds', 'data', allow_duplicate=True),
        Output('loading_screen', 'className'),
        Input('heartbeat_ds', 'data'),
        prevent_initial_call=True
    )
    def up(msg):
        if msg['data']['handshake']:
            return f'Heartbeat: {msg}', msg['data'],'hide'
        else:
            return f'Heartbeat: {msg}', msg['data'],'loading_screen'

# def create_startup_callback(app):    
#     @app.callback(
#         Output('loading_screen', 'className'),
#         Input('heartbeat_ds', 'n_intervals'),
#         prevent_initial_call=True
#     )
#     def hide_loader(msg, n_intervals):
#         if not msg:
#             heartbeat_item = gs.build_heart_beat_item(True, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'request_handshake', 'no_error')
#             item = gu.create_postbox_item('system', 'f_heartbeat', heartbeat_item)
#             print('create_startup_callback -> Sending initial heartbeat\n')
#             return 'loading_screen', item, False
#         else:
#             data = msg['data']
#             if msg['id'] == 'b_heartbeat' and data['status'] == 'backend_active':
#                 print('create_startup_callback -> Backend active, hiding loader\n')
#                 raise PreventUpdate
#             elif msg['id'] == 'b_heartbeat' and data['status'] == 'handshake_accepted':
#                 print('create_startup_callback -> Handshake accepted, hiding loader\n')
#                 return 'hide', no_update, True
#             else:
#                 raise PreventUpdate



