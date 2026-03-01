from dash_extensions.enrich import Input, Output

def create_active_callbacks(app):

    @app.callback(
            Output('set_po2_h1', 'children'),
            Input('set_po2_slider', 'value'),
            prevent_initial_call=True,
        )
    def po2_slider(val):
        return val
    
    @app.callback(
            Output('set_pco2_h1', 'children'),
            Input('set_pco2_slider', 'value'),
            prevent_initial_call=True,
        )
    def pco2_slider(val):
        return val