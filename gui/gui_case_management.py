from dash import Input, Output, State
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
        # State("case_number", "data"),
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
        # Input("ncm_confirm_btn", "n_clicks"),
        Input("inbox", "data"),
        State("cm_dropdown", "options"),
        # State("new_case_h1", "children"),
        State("ncm_input", "value"),
        prevent_initial_call=True,
    )
    def load_cm(data, drp_dwn_opt, ncn):
        #takes data from case-store, puts it to dropdown
        print(f'\ncase number list : {data}\n')
        if data and isinstance(data, dict) and data['msg_type'] == 'case_number' and data['id'] == 'cn_list':
            case_data = data['data']
            if isinstance(case_data, list):
                max_cn = 0
                new_cn_options = []
                for numb in case_data:
                    if isinstance(numb, int):
                        if numb > max_cn:
                            max_cn = numb
                            new_cn_options.append(str(numb))
                    else:
                        print('currupt data in casenumber list : ', numb)
                return new_cn_options
        # if new_case_h1 == "Number is valid, press confirm":
        #     drp_dwn_opt.append(ncn)
        #     return drp_dwn_opt
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
        if val:
            post_item = gu.create_postbox_item('case_number', 'cn_asgn', val)
            return post_item, True
        else:
            return None, False

    @app.callback(
        Output("new_case_h1", "children"),
        Input("ncm_input", "value"),
        State("cm_dropdown", "options"),
        prevent_initial_call=True,
    )
    def cm_new_case(input_val, cn_dropdown_options):
        cn_check = check_case_number(cn_dropdown_options, input_val)
        print(f'\ncn check : {cn_check}')
        if check_case_number(cn_dropdown_options, input_val):
            return "Number already assinged"
        elif not cn_dropdown_options:
            return "Case number list was not updated"
        else:
            print(f'number {input_val} is valid\n')
            return "Number is valid, press confirm"

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
        elif not nc_mdl_hidden and h1_child == "Number is valid, press confirm":
            return 0, True
        else:
            return 0, False

    @app.callback(
        Output("cm_dropdown", "value"),
        Input("ncm_close_btn", "n_clicks"),
        State("ncm_input", "value"),
        State("new_case_h1", "children"),
    )
    def confirm_ncn(nc_confirm_btn, nc_input, nc_h1):
        if nc_h1 == "Number is valid, press confirm":
            print(f'option value : {nc_input}')
            return nc_input
        else:
            None

    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Input("start_case_btn", "n_clicks"),
        State("sys_state", "data"),
        prevent_initial_call=True,
    )
    def start_case(sc_btn, sys_state):
        print(f'drop Value : {sys_state}')
        if sys_state and isinstance(sys_state, dict):
            cn = sys_state['system']['case_number']
            if cn != 0:
                send_item = gu.create_postbox_item('case_number', 'start_perfusion', 10)
                print(send_item)
                return None
        else: None