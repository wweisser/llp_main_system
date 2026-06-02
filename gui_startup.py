from datetime import datetime
from dash import dash, html, dcc, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
import gui_utils as gu
import gui_state as gs

def create_startup_screen():
    ret = (html.Div([
            html.Span('System starting ...'),
            html.Span(id='loader', className='loader')
        ], id='loading_screen', className='loading_screen'))
    return ret

def create_startup_callback(app):    
    @app.callback(
        Output('loading_screen', 'className'),
        Output('postbox', 'data'),
        Output('heartbeat_interval', 'disabled'),
        Input('heartbeat_data_store', 'data'),
        Input('heartbeat_interval', 'n_intervals'),
        prevent_initial_call=True
    )
    def hide_loader(msg, n_intervals):
        if not msg:
            heartbeat_item = gs.build_heart_beat_item(True, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'request_handshake', 'no_error')
            item = gu.create_postbox_item('system', 'f_heartbeat', heartbeat_item)
            print('create_startup_callback -> Sending initial heartbeat\n')
            return 'loading_screen', item, False
        
        data = msg['data']
        if msg['id'] == 'b_heartbeat' and data['status'] == 'backend_active':
            print('create_startup_callback -> Backend active, hiding loader\n')
            raise PreventUpdate
        elif msg['id'] == 'b_heartbeat' and data['status'] == 'handshake_accepted':
            print('create_startup_callback -> Handshake accepted, hiding loader\n')
            return 'hide', no_update, True
        else:
            raise PreventUpdate


if __name__ == '__main__':
    gui_app = dash.Dash(__name__)
    tailscale_ip =  '100.94.159.38'

    gui_app.layout = create_startup_screen()
    print('Startup screen was created')
    gui_app.run(host="127.0.0.1", port=8050, debug=True)
