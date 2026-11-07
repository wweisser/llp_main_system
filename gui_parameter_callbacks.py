from dash import Input, Output, html, State 
from dash.exceptions import PreventUpdate
import gui_utils as gu
import gui_case_management as gcm
import gui_panels as gp
import datetime

def tabbar_callbacks(app):
    @app.callback(
        Output('cntrl_cm_upper', 'children'),
        Input('inbox', 'data'),
        prevent_initial_call=True,
    )
    def update_case_id(msg):
        if isinstance(msg, dict) and msg['msg_type'] == 'system' and msg['id'] == 'state':
            return msg['system']['case_number']
        else: 
            return ""
    
    @app.callback(
        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def update_perfsuion_state(perfusion_time, perfusion_mode):
        clock_time = datetime.time()
        return perfusion_time, perfusion_mode, clock_time
    

def heartbeat_to_button(app, parameter, btn_I, btn_II):
    @app.callback(
        Output(btn_I, 'children'),
        Output(btn_II, 'children'),
        Input('heartbeat_data_store', 'data'),
        State('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def process(msg, state):
        try:
            if isinstance(msg, dict) and msg.get('msg_type') == 'heartbeat':
                data = msg['data']
                ct = data['last_heartbeat']
            else:
                ct = "---"
            if state and isinstance(state, dict) and state['data']['system']['start_time'] != 0:
                st = state['data']['system']['start_time']
                pt = datetime.now() - datetime.strptime(st, "%Y.%m.%d %H:%M:%S")
            else:
                pt = "---"
            return ct, pt
        except Exception as e:
            print(f'heartbeat_to_button -> error during heartbeat processing: {e}')
            raise PreventUpdate
        

def update_clocktime(app, clocktime_id):
    @app.callback(
        Output(clocktime_id, 'children'),
        Input('heartbeat_data_store', 'data')
    )
    def up(data):
        time = data.get('last_heartbeat')
        if time:
            dt_objekt = datetime.fromtimestamp(time)
            datum_string = dt_objekt.strftime("%Y-%m-%d %H:%M:%S")
            return datum_string
        else: 
            return None

def state_to_button(app):
    @app.callback(
        Output('art_po2', 'children'),
        Output('art_ph', 'children'),
        Output('art_pco2', 'children'),
        Output('hco3', 'children'),
        Output('base', 'children'),
        Output('cso2', 'children'),
        Output('k', 'children'),
        Output('vo2', 'children'),
        Output('ven_ph', 'children'),
        Output('ven_pco2', 'children'),
        Output('ven_po2', 'children'),
        Output('hct', 'children'),
        Output('hb', 'children'),
        Output('lactate', 'children'),
        Output('glucose', 'children'),

        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def cdi_callback(msg):
        try:
            if msg['id'] == 'state' and msg['data']['cdi']:
                return msg['data']['cdi']
            else:
                raise PreventUpdate
        except Exception as e:
            return print(f'cdi_callback {e}')

    @app.callback(
        Output('art_flow', 'children'),
        Output('art_pressure', 'children'),
        Output('art_temp', 'children'),
        Output('ven_flow', 'children'),
        Output('ven_pressure', 'children'),
        Output('ven_temp', 'children'),

        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def pump_callback(msg):
        try:
            if msg['id'] == 'state' and msg['data']['pump']:
                return msg['data']['pump']
            else:
                raise PreventUpdate
        except Exception as e:
            return print(f'cdi_callback {e}')

    @app.callback(
        Output('gbm_align_btn', 'className'),

        Output('set_fio2_slider', 'disabled'),
        Output('set_gas_flow_slider', 'disabled'),
        Output('set_po2_slider', 'disabled'),
        Output('set_pco2_slider', 'disabled'),

        Output('set_fio2_slider', 'value'),
        Output('set_gas_flow_slider', 'value'),

        Output('set_gas_flow', 'children'),
        Output('set_fio2', 'children'),
        Output('set_o2_flow', 'children'),
        Output('set_air_flow', 'children'),
        Output('gas_flow', 'children'),
        Output('fio2', 'children'),
        Output('air_flow', 'children'),
        Output('oxygen_flow', 'children'),

        Input('state_data_store', 'data'),
        prevent_initial_call=True,
    )
    def gbm_callback(msg):
        try:
            if msg['id'] == 'state' and msg['data']['gbm']:
                data = msg['data']['gbm']
                ret = {
                    'gbm_align_btn': "",
                    'set_fio2_slider': {
                        'disabled': data['gbm_align'],
                        'value': data['set_fio2'],
                    },
                    'set_gas_flow_slider': {
                        'disabled': data['gbm_align'],
                        'value': data['set_gas_flow'],
                    },
                    'set_po2_slider': {
                        data['gbm_align'],
                    },
                    'set_pco2_slider': {
                        data['gbm_align'],
                    },
                    'set_gas_flow': data['set_gas_flow'],
                    'set_fio2': data['set_fio2'],
                    'set_o2_flow': data['set_oxygen_flow'],
                    'set_air_flow':  data['set_oxygen_flow'],
                    'gas_flow': data['gas_flow'],
                    'fio2': data['fio2'],
                    'air_flow': data['air_flow'],
                    'oxygen_flow': data['oxygen_flow'],
                    }
                if data['gbm_align']:
                    ret['gbm_align_btn'] = 'align_btn_on'
                else:
                    ret['gbm_align_btn'] = 'align_btn_off'
                return ret
            else:
                raise PreventUpdate
        except Exception as e:
            print(f'cdi_callback {e}')
            raise PreventUpdate
        
