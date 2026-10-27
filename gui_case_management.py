from dash import Input, Output, State, no_update
import gui_utils as gu
from datetime import datetime

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

def case_manager_callbacks(app):

#opens csm modal and sends list request. Also closes mdl and sends asinged case id to backend.
    @app.callback(
        Output('case_mgr_mdl', 'className'),
        Output('postbox', 'data', allow_duplicate=True),
        Input('case_manager_btn', "n_clicks"),
        Input('cm_confirm_btn', 'n_clicks'),
        State('case_mgr_mdl', 'className'),
        State('case_id_dropdown', 'value'),
        prevent_initial_call=True,
    )
    def csm_button(cmb_click, ccb_click, class_name, asigned_case_id):
        if class_name == 'hide':
            disp_item = gu.dispatch('case_id', 'list_request')
            return 'case_mgr_mdl', disp_item
        else:
            if isinstance(asigned_case_id, int):
                disp_item = gu.dispatch('case_id', 'cn_asgn', asigned_case_id)
                return 'hide', disp_item
            return 'hide', no_update

#reacts on list form the backend and updates the case cid_list
    @app.callback(
        Output('case_id_dropdown', 'options'),
        Output('ncm_confirm_btn', 'n_clicks'),
        Input('case_id_store', 'data'),
        Input('ncm_confirm_btn', 'n_clicks'),
        State('ncm_input', 'value'),
        prevent_initial_call=True,
    )
    def fill_dropdown(msg, conf_new_cid_btn, new_cid):
        case_list = []
        if msg['id'] == 'cn_list':
            case_list = msg['data']
            if conf_new_cid_btn:
                case_list.append(new_cid)
        return case_list, 0
        
#opens new_case_id_mdl
    @app.callback(
        Output('new_case_mld', 'className'),
        Output('ncm_input', 'value'),
        Input('cm_new_case_button', 'n_clicks'),
        Input('ncm_close_btn', 'n_clicks'),
        State('new_case_mld', 'className'),
        State('new_case_h1', 'children'),
        prevent_initial_call=True,
    )
    def new_case_mdl(open_click, close_click, ncm_class_Name, cn_validity):
        if ncm_class_Name == 'hide':
            return 'new_case_mdl', ''
        else:
            return 'hide', no_update

    #checks and assigns new case_id to cid_list
    @app.callback(
        Output('new_case_h1', 'children'),
        Output('ncm_confirm_btn', 'disabled'),
        Input('ncm_input', 'value'),
        State('case_id_dropdown', 'options'),
        prevent_initial_call=True,
    )
    def cid_input_parser(input, cid_list):
        if input.isdigit():
            new_cid = int(input)
            if new_cid in cid_list:
                return 'case id does already exist', True
            else:
                return 'case id valid', False
        else:
            return 'please enter numeric value', True

    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Input('start_case_btn', 'n_clicks'),
        State('case_id_dropdown', 'value'),
        prevent_initial_call=True,
    )
    def start_case(start_case_btn, case_id):
        if case_id != None and case_id != 0:
            disp_item = gu.dispatch('system', 'start_case')
            return disp_item


