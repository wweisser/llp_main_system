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
        prevent_initial_call=True,
    )
    def csm_button(btn_click, modal_close_btn, hidden):
        if hidden:
            post_item = gu.create_postbox_item('case_number','list_request', '')
            print('Case number list request was send')
            return post_item, False
        else:
            print('modal is hidden again')
            return None, True


    @app.callback(
        Output("cm_dropdown", "options"),
        # Input("ncm_confirm_btn", "n_clicks"),
        Input("case_number", "data"),
        State("cm_dropdown", "options"),
        State("new_case_h1", "children"),
        State("ncm_input", "value"),
        prevent_initial_call=True,
    )
    def load_cm(case_data, drp_dwn_opt, new_case_h1, ncn):
        #takes data from case-store, puts it to dropdown
        print('\ncase number list : ', case_data)
        if isinstance(case_data, list):
            cn_options = []
            max_cn = 0
            for numb in case_data:
                if isinstance(numb, int):
                    if numb > max_cn:
                        max_cn = numb
                        cn_options.append(str(numb))
                else:
                    print('currupt data in casenumber list : ', numb)
            return cn_options
        if new_case_h1 == "Number is valid, press confirm":
            drp_dwn_opt.append(ncn)
            return drp_dwn_opt
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
        Output("cm_dropdown", "value"),
        Input("ncm_input", "value"),
        State("cm_dropdown", "options"),
        State("cm_dropdown", "value"),
        prevent_initial_call=True,
    )
    def cm_new_case(input_val, cn_dropdown_options, cn_dropdown_value):
        if check_case_number(cn_dropdown_options, input_val):
            return "Number already assinged", cn_dropdown_value
        elif not cn_dropdown_options:
            return "Case number list was not updated", None
        return "Number is valid, press confirm", cn_dropdown_value

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
        if not nc_mdl_hidden and nc_close_btn:
            print(nc_close_btn)
            return 0, True
        elif not nc_mdl_hidden and h1_child == "Number is valid, press confirm":
            return 0, True
        else:
            return 0, False


    @app.callback(
        Output("postbox", "data", allow_duplicate=True),
        Input("start_case_btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def start_case():
        post_item = gu.create_postbox_item('case_number', 'start_perfusion', 10)
        return post_item