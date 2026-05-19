from dash import Input, Output, State, no_update
import gui_utils as gu

def check_case_number(cn_arr, numb):
    if cn_arr:
        for cn in cn_arr:
            if numb == cn:
                return True
    return False

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

def case_manager_callbacks(app, button):
        
    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Output("case_mgr_mdl", "hidden", allow_duplicate=True),
        Input(button, "n_clicks"),
        State("case_mgr_mdl", "hidden"),
        prevent_initial_call=True,
    )
    def csm_button(btn_click, hidden):
        if hidden:
            post_item = gu.create_postbox_item('case_number','list_request', '')
            print('csm_button -> casenumber list request : ', post_item)
            return post_item, False
        else:
            print('modal is hidden again')
            return None, True


    @app.callback(
        Output("cm_dropdown", "options"),
        Input("case_id_store", "data"),
        prevent_initial_call=True,
    )
    def load_cm(msg):
        print(f'load_cm -> {msg}')

        if msg and isinstance(msg, dict) and msg['msg_type'] == 'case_number':
            case_id_list = parse_case_id(msg)
            print(f'\ncase_id_list : {case_id_list}\n')
            return case_id_list
        elif msg and isinstance(msg, list):
            return msg
        else:
            print('casenumber list in case_store item was not a list')
            print(msg)
            return []


    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Output("case_mgr_mdl", "hidden", allow_duplicate=True),
        Input("cm_confirm_btn", "n_clicks"),
        State("cm_dropdown", "value"),
        prevent_initial_call=True,
    )
    def confirm_btn(confirm_btn_click, val):
        #sends the current value of the dropdown via websocket
        print('asinged value : ', val)
        if val:
            post_item = gu.create_postbox_item('case_number', 'cn_asgn', val)
            return post_item, True
        else:
            return None, False

    @app.callback(
        Output("ncm_close_btn", "n_clicks"),
        Output("new_case_mld", "hidden"),
        Input("cm_new_case_button", "n_clicks"),
        Input("ncm_close_btn", "n_clicks"),
        Input("ncm_confirm_btn", "n_clicks"),
        State("new_case_mld", "hidden"),
        State("new_case_h1", "children"),
        prevent_initial_call=True,
    )
    def close_new_case_mdl(nc_btn, nc_close_btn, nc_confirm_btn, nc_mdl_hidden, h1_child):
        print(f'\nNew Case H1 : {h1_child}\n')
        if not nc_mdl_hidden and nc_close_btn:
            return 0, True
        elif not nc_mdl_hidden and h1_child == "Number was added to ID-list. Press Close":
            return 0, True
        else:
            return 0, False

    @app.callback(
        Output("case_id_store", "data", allow_duplicate=True),
        Output("new_case_h1", "children"),
        Input("ncm_confirm_btn", "n_clicks"),
        State("ncm_input", "value"),
        State("case_id_store", "data"),
        prevent_initial_call=True,
    )
    def cm_new_case(ncn_confirm_btn, input_val, case_id_item):
        if input_val.isdigit():
            case_id_list = case_id_item['data']
            cn_check = check_case_number(case_id_list, input_val)
            print(f'cn check : {cn_check}')
            if check_case_number(case_id_list, input_val):
                return no_update, "Number already assinged"
            elif not case_id_list:
                return no_update, "Case number list was not updated"
            else:
                case_id_list.append(input_val)
                print(f'cm_new_case -> number {input_val} is valid\n')
                return case_id_list, "Number was added to ID-list. Press Close"
        else:
            return no_update, 'Entry is not a digit'

    @app.callback(
        Output("start_case_btn", "children"),     
        Output("hope_btn", "disabled"),
        Output("cor_btn", "disabled"),
        Output("nmp_btn", "disabled"),
        Output("start_case_btn", "disabled"),
        Output("cm_new_case_button", "disabled"),
        Output("cm_confirm_btn", "disabled"),  
        Input("state_data_store", "data"),
        prevent_initial_call=True,
    )
    def disable_csm(msg):
        if msg['id'] == 'state':
            cn = msg['data']['system']['case_number']
            autosave = msg['data']['system']['autosave']
            if cn == 0 and not autosave:
                return "Start Case", True, True, True, True, False, False
            elif cn != 0 and not autosave:
                return "Start Case", True, True, True, False, False, False
            elif autosave:
                return "Stop Case", False, False, False, False, True, True
        else: 
            return no_update, no_update, no_update , no_update , no_update , no_update , no_update 


    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Input("start_case_btn", "n_clicks"),
        State("state_data_store", "data"),
        prevent_initial_call=True,
    )
    def start_case(sc_btn, msg):
        if msg['id'] == 'state':
            cn = msg['data']['system']['case_number']
            autosave = msg['data']['system']['autosave']
            if cn != 0 and not autosave:
                send_item = gu.create_postbox_item('archive', 'start_record', 10)
                print(send_item)
                return send_item
            elif autosave:
                send_item = gu.create_postbox_item('archive', 'stop_record', "")
                return send_item 
            else:
                return no_update
        else:
            return no_update
