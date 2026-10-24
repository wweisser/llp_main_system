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
        dcc.Store(id='state_ds', storage_type='session', data={'handshake': False}),

        dcc.Store(id='metabolic_graph_store', storage_type='memory'),
        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory'),
        dcc.Store(id='note_data_store', storage_type='memory'),
        dcc.Store(id='system_data_store', storage_type='memory'),
    ]))

def create_heartbeat_intervall(hb_rythm:int = None):
    if not hb_rythm:
        hb_rythm = 3000
    intervall = (html.Div([
        dcc.Interval(id='heartbeat_rhythm', interval=hb_rythm)
    ]))
    print(f'create_heartbeat_intervall -> heartbeat_rhythm initiated')
    return intervall

def create_startup_screen(test_env: bool):
    if test_env:
        cn = 'hide'
    else:
        cn = 'loading_screen'
    ret = (html.Div([
            html.Span('waitng for frontend response ...'),
            html.Span(id='loader', className='loader')
        ], id='loading_screen', className=cn))
    return ret

def beat(handshake:bool, last_heartbeat:int, status:str = None, error_state:str = None):
    """returns a sendable dispach item, containing a beat with information about the frontend state"""
    beat_msg = {
        'handshake': handshake,
        'last_heartbeat': last_heartbeat,
        'time': int(time.time()),
        'status': status,
        'error_state': error_state,
    }
    return beat_msg

def create_heartbeat_callback(app):
    """creates funktion, that sends heartbeatitem to the postbox to request handshake.
    When handshake state true, sends continous heartbeat without request"""
    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Input('heartbeat_rhythm', 'n_intervals'),
        State('state_ds', 'data'),
        prevent_initial_call=True
    )
    def f_heartbeat(n_intervals, state_ds):
        # print(f'create_heartbeat_callback -> {state_ds}\n')
        if state_ds['handshake'] == True:
            beat_msg = beat(True, int(time.time()))
        else:
            beat_msg = beat(False, int(time.time()), status='request_handshake')
            # print(f'create_heartbeat_callback -> initial beat was created')
        bltn = gu.dispatch(msg_type='system', id='f_heartbeat', data=beat_msg)
        return bltn

def hide_looding_screen(app, test_mode: bool):
    """listens to the heartbeat_ds, hides loader if handshake is accapted and changes handshake status in state_ds"""
    print(f'create_startup_callback -> initiated')
    @app.callback(
        Output('loading_screen', 'className'),
        Output('state_ds', 'data', allow_duplicate=True),
        Input('heatbeat_ds', 'data'),
        State('state_ds', 'data'),
        prevent_initial_call=True
    )
    def hide_loader(msg, state_ds):
        print(f'hide_looding_screen -> state_ds: {state_ds}\n')
        if msg and msg['data']:
            data = msg['data']
            print(f'data: {data}\n, status: {data['status']}\n')
            # if state_ds['t_env'] == True:
            #     return 'hide', no_update
            if data['status'] == 'handshake_accepted':
                print('hide_looding_screen -> Backend active, hiding loader\n')
                state_ds['handshake'] = True
                return 'hide', state_ds
        else:
            heartbeat_dispatch = beat(False, int(datetime.now().timestamp()), 'request_handshake')
            return 'loading_screen', heartbeat_dispatch

def gui_state_parser(app, test_mode: bool):
    create_heartbeat_callback(app)
    hide_looding_screen(app, test_mode)



    # @app.callback(
    #     Output('clock_time', 'children'),
    #     Output('state_ds', 'data', allow_duplicate=True),
    #     Output('loading_screen', 'className'),
    #     Input('heartbeat_ds', 'data'),
    #     prevent_initial_call=True
    # )
    # def up(msg):
    #     print(f'create_heartbeat_callback -> {msg}')
    #     if msg['data']['handshake']:
    #         return f'Heartbeat: {msg}', msg['data'],'hide'
    #     else:
    #         return f'Heartbeat: {msg}', msg['data'],'loading_screen'

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



