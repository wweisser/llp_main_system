from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import gui_panels as gp
import gui_utils as gu



def tabbar_callback(app):
    @app.callback(
        Output('drop_down_menu', 'className'),
            
        Output('perf_stat_panel', 'className'),
        Output('ph_panel', 'className'),
        Output('respiratory_panel', 'className'),
        Output('bga_entry_panel', 'className'),
        Output('permanent_panel', 'className'),

        Output('tab1_btn', 'n_clicks'),
        Output('tab2_btn', 'n_clicks'),
        Output('tab3_btn', 'n_clicks'),
        Output('tab4_btn', 'n_clicks'),
        Output('tab5_btn', 'n_clicks'),
        # Output('tab6_btn', 'n_clicks'),
        Input('tab1_btn', 'n_clicks'),
        Input('tab2_btn', 'n_clicks'),
        Input('tab3_btn', 'n_clicks'),
        Input('tab4_btn', 'n_clicks'),
        Input('tab5_btn', 'n_clicks'),
        # Input('tab6_btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def page_setter(btn1, btn2, btn3, btn4, btn5):
        hide = 'hide'
        show = 'side_panel_I'  # oder 'flex', je nach Layout

        if btn1:
            ret_arr = [show, hide, hide, hide, hide, hide]
        elif btn2:
            ret_arr = [hide, show, hide, hide, hide, 'side_panel_II']
        elif btn3:
            ret_arr = [hide, hide, show, hide, hide, 'side_panel_II']
        elif btn4:
            ret_arr = [hide, hide, hide, show, hide, 'side_panel_II']
        elif btn5:
            ret_arr = [hide, hide, hide, hide, 'bga_panel', 'side_panel_II']
        # elif btn6:
        #     ret_arr = [hide, hide, hide, hide, hide]

        btn_reset = [0, 0, 0, 0, 0]
        return ret_arr + btn_reset
  
    @app.callback(
        Output('note_mdl', 'hidden'),
        Input('note_mdl_btn', 'n_clicks'),
        State('note_mdl', 'hidden'),
        prevent_initial_call=True
    )
    def open_note_mdl(btn, hidden):
        print('hidden: ', hidden)
        if hidden:
            print('note mdl open')
            return False
        else:
            print('note mdl close')
            return True
    
    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Output('note_input', 'value'),
        Input('enter_note_btn', 'n_clicks'),
        State('note_input', 'value'),
        prevent_initial_call=True
    )
    def enter_note(btn, note):
        if note:
            item = gu.create_postbox_item('entry_request', 'note', note)
            return item, ""
        else:
            return None, ""

    # @app.callback(
    #     Output('note_h1', 'value', allow_duplicate=True),
    #     Input('state_data_store', 'data'),
    #     prevent_initial_call=True
    # )
    # def enter_note(sys_state):
    #     return sys_state['notes']

def bga_value_callback(app, val:str):
    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Input('store_btn', 'n_clicks'),
        Input(f'{val}_entry_field', 'value'),
        prevent_initial_call=True
    )
    def ship_bga_value(btn, val):
        if val and val.isdigit():
            return val
        else:
            raise PreventUpdate
