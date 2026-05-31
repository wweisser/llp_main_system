from dash import dash, html, dcc, Input, Output, State, no_update
import gui_utils as gu

def create_gui_state(startup_check, last_heartbeat, status, error_state):
    return {
        'startup_check': startup_check,
        'last_heartbeat': last_heartbeat,
        'status': status,
        'error_state': error_state,
    }

def create_msg_distribution():
    print('distribution stores created')
    return(html.Div([
        dcc.Store(id='postbox', storage_type='memory'),
        dcc.Store(id='inbox', storage_type='memory'),
        dcc.Store(id='metabolic_graph_store', storage_type='memory'),
        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory'),
        dcc.Store(id='note_data_store', storage_type='memory'),
        dcc.Store(id='system_data_store', storage_type='memory'),
        dcc.Store(id='heartbeat_data_store', storage_type='memory'),
        dcc.Store(id='gui_state_store', storage_type='memory')
    ]))

def create_heartbeat_intervall(app):
    intervall = (html.Div([
        dcc.Interval(id='heartbeat_interval', interval=1000)
    ]))
    return intervall

def create_f_heartbeat_callback(app):
    @app.callback(
        Output('postbox', 'data'),
        Output('gui_state_store', 'data'),
        State('gui_state_store', 'data'),
        Input('heartbeat_interval', 'n_intervals'),
        State('gui_state_store', 'data')
    )
    def f_heartbeat(n_intervals, gui_state):
        datetime = gu.get_current_time()
        if n_intervals == 0:
            datetime = gu.get_current_time()
            heartbeat_msg = create_gui_state(True, datetime, 'no_error')
            item = gu.create_postbox_item('system', 'f_heartbeat', heartbeat_msg)
            return item, heartbeat_msg
        else:
            item = gu.create_postbox_item('system', 'f_heartbeat', heartbeat_msg)
            return item, no_update
    