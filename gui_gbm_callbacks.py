from dash_extensions.enrich import Input, Output, State

def create_active_callbacks(app):
        
    @app.callback(
            Output('postbox', 'data'),

            Output('set_pco2', 'children'),
            Output('set_po2', 'children'),
            Output('set_air_flow', 'children'),
            Output('set_o2_flow', 'children'),

            Input('set_pco2_slider', 'value'),
            Input('set_po2_slider', 'value'),
            Input('set_air_flow_slider', 'value'),
            Input('set_o2_flow_slider', 'value'),
            prevent_initial_call=True,
        )
    def po2_slider(set_pco2, set_po2, set_air_flow, set_o2):
        params = [set_pco2, set_po2, set_air_flow, set_o2]
        gbm_command = f'{set_pco2}|{set_po2}|{set_air_flow}|{set_o2}'
        return params
    

