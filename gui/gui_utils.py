from dash_extensions.enrich import Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from dash import html, dcc
import json

def create_msg_distribution():
    print('distribution stores created')
    return(html.Div([
        dcc.Store(id='postbox'),
        dcc.Store(id='data_to_plot'),
        dcc.Store(id='sys_state'),
        dcc.Store(id='case_number')
    ]))

def create_postbox_item(msg_type: str, id: str, data):
    msg_item = {
        'msg_type': 'ux',
        'id': '',
        'data': ''
    }
    if msg_type:
        msg_item['msg_type'] = msg_type
    if id:
        msg_item['id'] = id
    if data:
        msg_item['data'] = data
    msg_item = json.dumps(msg_item)
    return msg_item

def ws_send(app):
    @app.callback(
        Output("ws", "send"), 
        Input("postbox", "data"),
        prevent_initial_call=True
    )
    def send(send_val):
        print('value to send : ', send_val, 'type : ', type(send_val))
        if isinstance(send_val, str):
            print('sended value : ', send_val)
            return send_val
        else:
            return '400'
        
def parse_ws_msg(msg: dict):
    if isinstance(msg, dict):
        msg_data = msg['data']
        data = json.loads(msg_data)
        # print(data['system']['case_number'])
        return data
    else: 
        return None
         

def ws_recv(app):
    @app.callback(
        Output("case_number", "data"), 
        Input("ws", "message"),
        prevent_initial_call=True
        )
    def distribute_case_msg(msg):
        data = parse_ws_msg(msg)
        if data and data['msg_type'] == 'case':
            return data['data']
        else:
            raise PreventUpdate
    
    @app.callback(
        Output("data_to_plot", "data"), 
        Input("ws", "message"),
        prevent_initial_call=True
        )
    def distribute_plot_msg(msg):
        data = parse_ws_msg(msg)
        if data and data['msg_type'] == 'plot':
            return data['data']
        else:
            raise PreventUpdate
    
    @app.callback(
        Output("sys_state", "data"), 
        Input("ws", "message"),
        prevent_initial_call=True
        )
    def distribute_system_msg(msg):
        data = parse_ws_msg(msg)
        if data and data['msg_type'] == 'system':
            return data['data']
        else:
            raise PreventUpdate
    
