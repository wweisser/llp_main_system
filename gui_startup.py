from datetime import datetime
from dash import dash, html, dcc, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
import gui_utils as gu
import gui_state as gs

def create_startup_screen():
    ret = (html.Div([
            html.Span('waitng for frontend response ...'),
            html.Span(id='loader', className='loader')
        ], id='loading_screen', className='loading_screen'))
    return ret

def create_startup_callback(app, test_mode: bool):
    """listens to the heartbeat_rhythm and sends a beat to postbox for each intervall, if a frontend response
    arrives in the loading screen is hidden""" 
    @app.callback(
        Output('loading_screen', 'className'),
        Output('postbox', 'data'),
        # Output('heartbeat_rythm', 'disabled'),
        State('state_ds', 'data'),
        Input('heartbeat_rhythm', 'n_intervals'),
        prevent_initial_call=True
    )
    def hide_loader(msg, n_intervals):
        if test_mode:
            return 'hide', no_update
        heartbeat_dispach = gs.beat(True, int(datetime.now().timestamp()), 'request_handshake')
        if msg:
            data = msg['data']
            if msg['id'] == 'b_heartbeat' and not data['status'] == 'error':
                print('create_startup_callback -> Backend active, hiding loader\n')
                return 'hide', heartbeat_dispach
        else:
            return 'loading_screen', heartbeat_dispach


if __name__ == '__main__':
    gui_app = dash.Dash(__name__)
    tailscale_ip =  '100.94.159.38'

    gui_app.layout = create_startup_screen()
    print('Startup screen was created')
    gui_app.run(host="127.0.0.1", port=8050, debug=True)
