from dash import Input, Output, State
from dash_extensions import EventSource
import gui_utils as gu
import gui_case_management as gcm
import gui_panels as gp
import datetime

def tabbar_callbacks(app):
    @app.callback(
        Output('cntrl_cm_upper', 'children'),
        Input('sys_state', 'data'),
        prevent_initial_call=True,
    )
    def update_case_id(sys_state):
        sys_state
        return case_number
    
    @app.callback(
        Input('sys_state', 'data'),
        prevent_initial_call=True,
    )
    def update_perfsuion_state(perfusion_time, perfusion_mode):
        clock_time = datetime.time()
        return perfusion_time, perfusion_mode, clock_time
    
    @app.callback(

    )
    def update_save_mode(save_interval, last_save):
        return save_interval, last_save
    
    # modify cm modal