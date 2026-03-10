from dash_extensions.enrich import Input, Output, State

def create_active_callbacks(app):

    @app.callback(
            Output('active_mdl', 'className'),
            Input('tab6_btn', 'n_clicks'),
            State('active_mdl', 'className'),
            prevent_initial_call=True,
        )
    def show_gas_controller(val, className):
        if className == "active_mdl":
            return "hide"
        else:
            return "active_mdl"
        
    @app.callback(
            Output('set_po2', 'children'),
            Input('set_po2_slider', 'value'),
            prevent_initial_call=True,
        )
    def po2_slider(val):
        return val
    
    @app.callback(
            Output('set_pco2', 'children'),
            Input('set_pco2_slider', 'value'),
            prevent_initial_call=True,
        )
    def pco2_slider(val):
        return val

    
    @app.callback(
            Output('set_air_flow', 'children'),
            Input('set_air_flow_slider', 'value'),
            prevent_initial_call=True,
        )
    def po2_slider(val):
        return val

    
    @app.callback(
            Output('set_o2_flow', 'children'),
            Input('set_o2_flow_slider', 'value'),
            prevent_initial_call=True,
        )
    def pco2_slider(val):
        return val
