from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate
import gui_panels as gp
import gui_utils as gu

# def slider_contoll(app, btn: str, slider_area: str):

#     @app.callback(
#         Output(slider_area, 'className'),
#         Input(btn, 'n_clicks'),

#         State(slider_area, 'className'),
#         prevent_initial_call=True
#     )
#     def set_slider(click, class_name):
#         print(class_name)
#         if class_name == 'slider_area':
#             return 'slider_area_active'
#         elif class_name == 'slider_area_active':
#             return 'slider_area'

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

def gbm_callbacks(app):
    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Input('gbm_align_btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def glm_align_btn(click):
        disp_item = gu.dispatch(msg_type='front_end_com', id='switch_align')
        return disp_item

    @app.callback(
        Output('set_po2_btn', 'n_clicks'),
        Output('set_pco2_btn', 'n_clicks'),
        Output('set_fio2_btn', 'n_clicks'),
        Output('set_gas_flow_btn', 'n_clicks'),

        Output('set_po2_slider', 'disabled'),
        Output('set_po2_slider_area', 'disabled'),

        Output('set_pco2_slider', 'disabled'),
        Output('set_pco2_slider_area', 'disabled'),

        Output('set_fio2_slider', 'disabled'),
        Output('set_fio2_slider_area', 'disabled'),

        Output('set_gas_flow_slider', 'disabled'),
        Output('set_gas_flow_slider_area', 'disabled'),

        Input('set_po2_btn', 'n_clicks'),
        Input('set_pco2_btn', 'n_clicks'),
        Input('set_fio2_btn', 'n_clicks'),
        Input('set_gas_flow_btn', 'n_clicks'),

        State('set_po2_slider', 'disabled'),
        State('set_pco2_slider', 'disabled'),
        State('set_fio2_slider', 'disabled'),
        State('set_gas_flow_slider', 'disabled'),
        State('gbm_align_btn', 'className'),
        prevent_initial_call=True
    )
    def set_slider_area(po2_btn, pco2_btn, fio2_btn, gas_flow_btn, po2_slider, pco2_slider, fio2_slider, gas_flow_slider, align):
        ret = [0, 0, 0, 0, True, True, True, True, True, True, True, True]
        if po2_btn and po2_slider and align == 'align_btn_on':
            ret[4] = False
            ret[5] = False
        elif pco2_btn and pco2_slider and align == 'align_btn_on':
            ret[6] = False
            ret[7] = False
        elif fio2_btn and fio2_slider and align == 'align_btn_off':
            ret[8] = False
            ret[9] = False
        elif gas_flow_btn and gas_flow_slider and align == 'align_btn_off':
            ret[10] = False
            ret[11] = False
        return ret


    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),

        Input('set_fio2_slider', 'value'),
        Input('set_gas_flow_slider', 'value'),
        Input('set_po2_slider', 'value'),
        Input('set_pco2_slider', 'value'),
        
        State('set_fio2_slider', 'disabled'),
        State('set_gas_flow_slider', 'disabled'),
        State('set_po2_slider', 'disabled'),
        State('set_pco2_slider', 'disabled'),

        prevent_initial_call=True
    )
    def glm_slider(set_fio2, set_gas_low, set_po2, set_pco2, set_fio2_slider, set_gas_flow_slider, set_po2_slider, set_pco2_slider):
        set_params = {
            'set_fio2': None,
            'set_gas_flow': None,
            'set_po2': None,
            'set_pco2': None
        }
        # print(f'glm_slider -> set_fio2: {set_fio2}, set_gas_low:{set_gas_low} set_fio2_slider: {set_fio2_slider}, set_gas_flow_slider:{set_gas_flow_slider}')

        if not set_fio2_slider:
            set_params['set_fio2'] = set_fio2
        elif not set_gas_flow_slider:
            set_params['set_gas_flow'] = set_gas_low
        elif not set_po2_slider:
            set_params['set_po2'] = set_po2
        elif not set_pco2_slider:
            set_params['set_pco2'] = set_pco2
        # print(f'glm_slider -> fio2: {set_fio2}, set_params:{set_params}')
        disp_item = gu.dispatch(msg_type='front_end_com', id='set_gbm_params', data=set_params)
        return disp_item
