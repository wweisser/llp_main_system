from dash_extensions.enrich import Input, Output, no_update
from dash import html, dcc, no_update
import json


#creates distribution stores and postbox
def create_msg_distribution():
    print('distribution stores created')
    return(html.Div([
        dcc.Store(id='postbox', storage_type='memory'),
        dcc.Store(id='inbox', storage_type='memory'),
        dcc.Store(id='metabolic_graph_store', storage_type='memory'),
        dcc.Store(id='state_data_store', storage_type='memory'),
        dcc.Store(id='case_id_store', storage_type='memory'),
        dcc.Store(id='note_data_store', storage_type='memory')

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

def gui_ws_send(app):
    @app.callback(
        Output("ws", "send"), 
        Input("postbox", "data"),
        prevent_initial_call=True
    )
    def send(send_val):
        if isinstance(send_val, str):
            print('gui_ws_send -> sended value : ', send_val)
            return send_val
        else:
            return no_update

def parse_ws_msg(msg: dict):
    if isinstance(msg, dict):
        msg_data = msg['data']
        data = json.loads(msg_data)
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
def gui_ws_recv(app):
    # @app.callback(
    #     Output("inbox", "data"), 
    #     Input("ws", "message"),
    #     prevent_initial_call=True
    #     )
    # def distribute_case_msg(msg):
    #     data = parse_ws_msg(msg)
    #     if data and isinstance(data, dict):
    #         # print(f"inbox -> {data['id']}")

    #         return data
    #     else:
    #         print("inbox -> corrupt inbox file")
    #         return no_update
        
    @app.callback(
        Output("state_data_store", "data"), 
        Output("case_id_store", "data"), 
        Output("metabolic_graph_store", "data"), 
        Output("note_data_store", "data"), 
        Input("ws", "message"),
        prevent_initial_call=True
    )
    def distribute_msg(msg):
        if isinstance(msg, dict):
            data = parse_ws_msg(msg)  # data ist ab hier dein dict
            try:
                if data and isinstance(data, dict):
                    msg_type = data.get('msg_type')
                    if msg_type == 'system':
                        return data, no_update, no_update, no_update
                    elif msg_type == 'case_number':
                        return no_update, data, no_update, no_update
                    elif msg_type == 'metabolic_graph_store':
                        return no_update, no_update, data, no_update
                    elif msg_type == 'notes':
                        return no_update, no_update, no_update, data
                    else:
                        print(f"distribute_msg -> unbekannter msg_type: {msg_type}")
                        return no_update, no_update, no_update, no_update
                else:
                    print("distribute_msg -> corrupt msg")
                    return no_update, no_update, no_update, no_update
            except Exception as e:
                print(f'distribute_msg -> error: {e} | raw: {msg}')
                return no_update, no_update, no_update, no_update
        else:
            print("distribute_msg -> corrupt msg")
            return no_update, no_update, no_update


