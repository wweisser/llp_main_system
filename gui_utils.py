from dash_extensions.enrich import Input, Output, no_update
from dash import html, dcc, no_update
import json
from datetime import datetime

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

#send functions
def dispatch(msg_type: str, id: str, data):
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

def create_send_callbacks(app):
    @app.callback(
        Output("ws", "send"), 
        Input("postbox", "data"),
        prevent_initial_call=True
    )
    def send(send_val):
        if isinstance(send_val, str):
            # print('gui_ws_send -> sended value : ', send_val)
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
                    
# reveive callbacks
def create_recv_callbacks(app):
    @app.callback(
        Output("state_data_store", "data"), 
        Output("case_id_store", "data"), 
        Output("note_data_store", "data"), 
        Output("metabolic_graph_store", "data"), 
        Output("system_data_store", "data"),
        Output("state_ds", "data"),
        Output("heatbeat_ds", "data"),
        Output("download_store", "data"),
        Input("ws", "message"),
        prevent_initial_call=True
    )
    def distribute_msg(msg):
        rl = {
            'state': no_update,
            'case_id': no_update,
            'metabolic_graph': no_update,
            'notes': no_update,
            'system': no_update,
            'gui_state': no_update,
            'heartbeat': no_update,
            'download': no_update
        }
        if isinstance(msg, dict):
            data = parse_ws_msg(msg)  # data ist ab hier dein dict
            try:
                # print(f'distribute_msg -> item received {datetime.now()}\nMessage : {msg}\n')
                if data and isinstance(data, dict):
                    msg_type = data.get('msg_type')
                    if msg_type == 'system':
                        rl['system'] = data
                    elif msg_type == 'case_id':
                        rl['case_id'] = data
                    elif msg_type == 'metabolic_graph':
                        rl['metabolic_graph'] = data
                    elif msg_type == 'notes':
                        rl['notes'] = data
                    elif msg_type == 'state':
                        rl['state'] = data
                    elif msg_type == 'gui_state':
                        rl['gui_state'] = data
                    elif msg_type == 'heartbeat':
                        rl['heartbeat'] = data
                    elif msg_type == 'download':
                        rl['download'] = data
                    else:
                        print(f"distribute_msg -> unbekannter msg_type: {msg_type}")
                    # print(f'create_heartbeat_callback -> {rl['heartbeat']}')
                else:
                    print("distribute_msg -> corrupt msg")
            except Exception as e:
                print(f'distribute_msg -> error: {e} | raw: {msg}')
            return rl['state'], rl['case_id'], rl['metabolic_graph'], rl['notes'], rl['system'], rl['gui_state'], rl['heartbeat'], rl['download']


