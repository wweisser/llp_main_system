from dash_extensions.enrich import Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from dash import html, dcc, no_update
import json


#creates distribution stores and postbox
def create_msg_distribution():
    print('distribution stores created')
    return(html.Div([
        dcc.Store(id='postbox', storage_type='memory'),
        dcc.Store(id='inbox', storage_type='memory'),
        dcc.Store(id='graph_data_store', storage_type='memory'),
        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory')
    ]))

#send functions

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

# reveive functions
# parser methods
def parse_ws_msg(msg: dict):
    if isinstance(msg, dict):
        msg_data = msg['data']
        data = json.loads(msg_data)
        print('UNPACKED DATA')
        print(f'\n hier kommt was an {data['msg_type']}')
        return data
    else: 
        return None
    
def parse_case_id(msg: dict):
    if msg['id'] == 'cn_list' and isinstance(msg['data'], list):
        cn_list = msg['data']
        inter_list = []
        for id in cn_list:
            if isinstance(id, int):
                is_in_list = False 
                for x in inter_list:
                    if x == id:
                        is_in_list = True
                if not is_in_list:
                    inter_list.append(id)
        drp_dwn_list = []
        for id in inter_list:
            drp_dwn_list.append(str(id))
        return drp_dwn_list
    else: 
        return None
                    
# reveive callbacks
def ws_recv(app):
    @app.callback(
        Output("inbox", "data"), 
        Input("ws", "message"),
        prevent_initial_call=True
        )
    def distribute_case_msg(msg):
        # print('\nRAW MESSAGE : ', msg)
        data = parse_ws_msg(msg)
        if data and isinstance(data, dict):
            return data
        else:
            print("inbox -> corrupt inbox file")
            return no_update


    @app.callback(
        Output("graph_data_store", "data"), 
        Input("inbox", "data"),
        prevent_initial_call=True
        )
    def distribute_plot_msg(msg):
        if msg and msg['msg_type'] == 'visual':
            # print(msg['data'])
            return msg['data']
        else:
            return no_update

    @app.callback(
        Output("state_data_store", "data"), 
        Input("inbox", "data"),
        prevent_initial_call=True
        )
    def distribute_system_msg(msg):
        if msg and msg['msg_type'] == 'system':
            # print(msg['data'])
            return msg
        else:
            return no_update

    @app.callback(
        Output("case_id_store", "data", allow_duplicate=True), 
        Input("inbox", "data"),
        prevent_initial_call=True
        )
    def distribute_system_msg(msg):
        print(f'inbox content {msg['msg_type']}\n')
        if msg and msg['msg_type'] == 'case_number':
            print(f'\n CASE DATA : {msg}\n')
            case_ids = parse_case_id(msg)
            if case_ids:
                print(f'case id list was created and fowarted to store')
                return case_ids
            else:
                return no_update
        else:
            return no_update
