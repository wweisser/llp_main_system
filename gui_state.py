from dash import html, dcc, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
import gui_utils as gu
import time


### Frage: wie muss das zusammenspiel zwischen beat in heartbeat_ds und state_ds gelöst werden, um ein sinnvollen hadshake zu erzeugen?

def create_msg_distribution():
    print('distribution stores created')
    initial_state = beat(handshake=False, last_heartbeat=0, status='request_handshake')
    return(html.Div([
        dcc.Store(id='postbox', storage_type='memory'),
        dcc.Store(id='inbox', storage_type='memory'),
        dcc.Store(id='download_store', storage_type='session'),

        dcc.Store(id='heartbeat_ds', storage_type='memory', data=initial_state),
        dcc.Store(id='state_ds', storage_type='memory'),

        dcc.Store(id='graphs_store', storage_type='memory'),
        dcc.Store(id='plot_store', storage_type='memory'),

        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory'),
        dcc.Store(id='note_data_store', storage_type='memory'),
        dcc.Store(id='system_data_store', storage_type='memory'),

        dcc.Interval(id='clock', interval=1000)
    ]))

def create_heartbeat_intervall(hb_rythm:int = None):
    if not hb_rythm:
        hb_rythm = 10000
    intervall = (html.Div([
        dcc.Interval(id='heartbeat_rhythm', interval=hb_rythm)
    ]))
    print(f'create_heartbeat_intervall -> heartbeat_rhythm initiated')
    return intervall

def create_startup_screen(test_mode: bool):
    if test_mode:
        cn = 'hide'
    else:
        cn = 'loading_screen'
    ret = (html.Div([
            html.Span('waiting for frontend response ...'),
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
        State('heartbeat_ds', 'data'),
        prevent_initial_call=True
    )
    def f_heartbeat(n_intervals, heartbeat):
        if heartbeat['handshake'] == True:
            beat_msg = beat(True, int(time.time()))
        else:
            # print(f'create_heartbeat_callback -> {heatbeat}\n')
            beat_msg = beat(False, int(time.time()), status='request_handshake')
            # print(f'create_heartbeat_callback -> initial beat was created')
        bltn = gu.dispatch(msg_type='system', id='f_heartbeat', data=beat_msg)
        return bltn

def hide_looding_screen(app):
    """listens to the heartbeat_ds, hides loader if handshake is accapted and changes handshake status in state_ds"""
    print(f'create_startup_callback -> initiated')
    @app.callback(
        Output('loading_screen', 'className'),
        Input('heartbeat_ds', 'data'),
        prevent_initial_call=True
    )
    def hide_loader(heartbeat):
        print(f'hide_looding_screen: data {heartbeat}\n')
        if heartbeat['status'] == 'handshake_accepted':
            print('hide_looding_screen -> Backend active, hiding loader\n')
            heartbeat['handshake'] = True
            return 'hide'
        else:
            return 'loading_screen'
    

def gui_state_parser(app):
    create_heartbeat_callback(app)
    hide_looding_screen(app)


