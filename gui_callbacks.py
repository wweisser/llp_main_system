from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import gui_panels as gp
import gui_utils as gu



def tabbar_callback(app):
    @app.callback(
        Output('data_panel', 'className'),
        Output('perfusion_panel', 'className'),
        Output('ph_panel', 'className'),
        Output('respiratory_panel', 'className'),
        Output('permanent_panel', 'className'),

        Output('tab1_btn', 'n_clicks'),
        Output('tab2_btn', 'n_clicks'),
        Output('tab3_btn', 'n_clicks'),
        Output('tab4_btn', 'n_clicks'),
        Output('tab5_btn', 'n_clicks'),

        Input('tab1_btn', 'n_clicks'),
        Input('tab2_btn', 'n_clicks'),
        Input('tab3_btn', 'n_clicks'),
        Input('tab4_btn', 'n_clicks'),
        Input('tab5_btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def page_setter(btn1, btn2, btn3, btn4, btn5):
        hide = 'hide'
        show = 'left_controlled_page' 

        if btn1:
            ret_arr = ['full_page', hide, hide, hide, hide]
        elif btn2:
            ret_arr = [hide, show, hide, hide, 'side_panel_II']
        elif btn3:
            ret_arr = [hide, hide, show, hide, 'side_panel_II']
        elif btn4:
            ret_arr = [hide, hide, hide, show, 'side_panel_II']
        elif btn5:
            ret_arr = [hide, hide, hide, hide, 'side_panel_II']
  

        btn_reset = [0, 0, 0, 0, 0]
        return ret_arr + btn_reset
  
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
