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

def ws_recv(app):
    @app.callback(
        Output("data_to_plot", "data"), 
        Output("sys_state", "data"), 
        Output("case_number", "data"),
        Input("ws", "message"),
        prevent_initial_call=True
        )
    def distribute_msg(msg):
        if msg:
            msg_data = msg['data']
            data = json.loads(msg_data)
            # Distribution of system state
            if data['msg_type'] == 'system':
                if data['id'] == 'state':
                    return no_update, data['data'], no_update
                elif data['id'] == 'val':
                    pass
                else:
                    pass
            # distribution of data to plot
            elif data['msg_type'] == 'plot':
                return data['data'], no_update, no_update
            # distrbution of case number related data
            elif data['msg_type'] == 'case':
                if data['id'] == 'cn_list':
                    return no_update, no_update, data['data'] 
            else:
                pass
        else:
            raise PreventUpdate
