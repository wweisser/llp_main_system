from dash import html, dcc, Input, Output
import plotly.express as px

def gui_update():
    return(html.Div([
        # updates gui
        dcc.Interval(id='gui_interval', interval=1000, n_intervals=0, disabled=False),
        # runs a counter is reset after 60 seconds. 
        dcc.Interval(id='case_interval', interval=1000, n_intervals=0, disabled=True)
        ])
    )

def reset_case_interval(app):
    @app.callback(
        Output('case_interval', 'n_intervals'),
        Input('case_interval', 'n_intervals'),
        prevent_initial_call=True
    )
    def reset_case_interval(n_intervals):
        if n_intervals < 60:
            return n_intervals
        else:
            return 0
