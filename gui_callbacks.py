from dash import Input, Output, State
from dash.exceptions import PreventUpdate
import gui_panels as gp
import gui_utils as gu

def tabbar_callback(app):
    @app.callback(
        Output('plot_panel', 'className'),
        Output('perfusion_panel', 'className'),
        Output('protocol_panel', 'className'),
        Output('data_panel', 'className'),
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

        if btn1:
            ret_arr = ['plot_panel', hide, hide, hide, hide]
        elif btn2:
            ret_arr = [hide, 'left_controlled_page', hide, hide, 'side_panel_II']
        elif btn3:
            ret_arr = [hide, hide, hide, 'protocol_panel', 'side_panel_II']
        elif btn4:
            ret_arr = [hide, hide, 'protocol_panel', hide, 'side_panel_II']
        elif btn5:
            ret_arr = [hide, hide, hide, hide, 'side_panel_II']
  

        btn_reset = [0, 0, 0, 0, 0]
        return ret_arr + btn_reset
  
    @app.callback(
        Output('com_panel', 'className'),
        Input('vent_mdl_btn', 'n_clicks'),
        State('com_panel', 'className'),
        prevent_initial_call=True
    )
    def opne_gbm_panel(n_clicks, open_state):
        if open_state == 'hide':
            return 'com_panel'
        else:
            return 'hide'
