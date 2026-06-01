from dash import dash, html, dcc, Input, Output, no_update
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
        Output('heartbeat_data_store', 'data', allow_duplicate=True),
        Input('heartbeat_data_store', 'data'),
        prevent_initial_call=True
    )
    def hide_loader(msg):
        if msg['id'] == 'b_heartbeat' and msg['data']['status'] == 'backend_active':
            print('create_startup_callback -> Handshake accepted, hiding loader\n')
            datetime = gu.get_current_time()
            heartbeat_msg = gs.create_gui_state(False, datetime, 'handshake_accepted', 'no_error')
            return 'hide', heartbeat_msg
        else:
            heartbeat_msg = gs.create_gui_state(False, datetime, 'handshake_pending', 'no_error')
            return 'loading_screen', heartbeat_msg


if __name__ == '__main__':
    gui_app = dash.Dash(__name__)
    tailscale_ip =  '100.94.159.38'

    gui_app.layout = create_startup_screen()
    print('Startup screen was created')
    gui_app.run(host="127.0.0.1", port=8050, debug=True)
