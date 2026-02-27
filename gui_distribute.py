# from dash_extensions.enrich import Input, Output

# def distribute_state(app):
#     @app.callback(
#         Output('module', 'children'),
#         Input('state_data_store', 'data'),
#         prevent_initial_call=True
#     )
#     def asign_sate(data):
#         return str(data)