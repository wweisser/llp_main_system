from dash import Input, Output, State, no_update
import gui_utils as gu

def check_case_number(cn_arr, numb):
    if cn_arr:
        for cn in cn_arr:
            if numb == cn:
                return True
    return False

def case_manager_callbacks(app, button):
        
    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Output("case_mgr_mdl", "hidden", allow_duplicate=True),
        Input(button, "n_clicks"),
        Input("cm_close_btn", "n_clicks"),
        State("case_mgr_mdl", "hidden"),
        prevent_initial_call=True,
    )
    def csm_button(btn_click, modal_close_btn, hidden):
        if hidden:
            post_item = gu.create_postbox_item('case_number','list_request', '')
            print('Case number list request was send')
            # print('\n current data : ', data)
            return post_item, False
        else:
            print('modal is hidden again')
            return None, True


    @app.callback(
        Output("cm_dropdown", "options"),
        Input("case_id_store", "data"),
        prevent_initial_call=True,
    )
    def load_cm(case_id_list):
        #takes data from case-store, puts it to dropdown
        print(f'\ncase_id_list : {case_id_list}\n')
        if case_id_list and isinstance(case_id_list, list):
            return case_id_list
        else:
            print('casenumber list in case_store item was not a list')
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
    def cm_new_case(ncn_confirm_btn, input_val, case_id_list):
        if input_val.isdigit():
            cn_check = check_case_number(case_id_list, input_val)
            print(f'cn check : {cn_check}')
            if check_case_number(case_id_list, input_val):
                return no_update, "Number already assinged"
            elif not case_id_list:
                return no_update, "Case number list was not updated"
            else:
                case_id_list.append(input_val)
                print(f'number {input_val} is valid\n')
                return case_id_list, "Number was added to ID-list. Press Close"
        else:
            return no_update, 'Entry is not a digit'

    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Input("start_case_btn", "n_clicks"),
        State("state_data_store", "data"),
        prevent_initial_call=True,
    )
    def start_case(sc_btn, sys_state):
        print(f'drop Value : {sys_state}')
        if sys_state and isinstance(sys_state, dict):
            cn = sys_state['data']['system']['case_number']
            if cn != 0:
                send_item = gu.create_postbox_item('case_number', 'start_perfusion', 10)
                print(send_item)
                return None
        else: None