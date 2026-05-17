from dash_extensions.enrich import Input, Output, State

def create_active_callbacks(app):
    @app.callback(
        Output('download_mdl', 'className'),
        Input('download_mdl_btn', 'n_clicks'),
        State('download_mdl', 'className'),
        prevent_initial_call=True,
    )
    def show_gas_controller(n_clicks, className):
        if className == "download_mdl":
            return "hide"
        else:
            return "download_mdl"