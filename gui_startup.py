from dash import dash, html, dcc, Input, Output, no_update
import gui_utils as gu

def create_msg_distribution():
    print('distribution stores created')
    return(html.Div([
        dcc.Store(id='postbox', storage_type='memory'),
        dcc.Store(id='inbox', storage_type='memory'),
        dcc.Store(id='metabolic_graph_store', storage_type='memory'),
        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory'),
        dcc.Store(id='note_data_store', storage_type='memory'),
        dcc.Store(id='system_data_store', storage_type='memory')
    ]))

def strartup_screen_gui(app):
    ret = (html.Div([
            html.Span('Perfusion System starting up...'),
            html.Span(id='loader', className='loader')
        ], id='loading_screen', className='loading_screen'))

    @app.callback(
        Output('postbox', 'data'),
        Input('state_data_store', 'data'),
    )
    def hide_loader(msg):
        item = gu.create_postbox_item('system', 'startup', 'ux setup in progress')
        return item
    
    @app.callback(
        Output('loading_screen', 'style'),
        Input('system_data_store', 'data'),
    )
    def hide_loader(msg):
        if msg['id'] == 'backend_status' and msg['data'] == 'ready':
            return 'hide'
        return 'loading_screen'

    return ret


if __name__ == '__main__':
    gui_app = dash.Dash(__name__)
    tailscale_ip =  '100.94.159.38'
    gui_app.layout = strartup_screen_gui()
    print('Startup screen was created')
    gui_app.run(host="127.0.0.1", port=8050, debug=True)
