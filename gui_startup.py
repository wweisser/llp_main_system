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
    print(f'create_startup_callback -> initiated')
    @app.callback(
        Output('loading_screen', 'className'),
        Output('state_ds', 'data', allow_duplicate=True),
        Input('heatbeat_ds', 'data'),
        prevent_initial_call=True
    )
    def hide_loader(msg, n_intervals):
        print(f'create_startup_callback -> {msg}')
        if test_mode:
            return 'hide', no_update
        elif msg and msg['data']:
            data = msg['data']
            if msg['id'] == 'bcknd_heartbeat' and data['status'] == 'handshake_accepted':
                print('create_startup_callback -> Backend active, hiding loader\n')
                return 'hide', no_update
        else:
            heartbeat_dispach = gs.beat(False, int(datetime.now().timestamp()), 'request_handshake')
            return 'loading_screen', heartbeat_dispach

    # @app.callback(
    #     Output('postbox', 'data'),
    #     Input('heartbeat_rhythm', 'n_intervals'),
    #     State('state_ds', 'data')
    # )
    # def pace_maker(ping, state_ds):
    #     pass


if __name__ == '__main__':
    gui_app = dash.Dash(__name__)
    tailscale_ip =  '100.94.159.38'

    gui_app.layout = create_startup_screen()
    print('Startup screen was created')
    gui_app.run(host="127.0.0.1", port=8050, debug=True)
