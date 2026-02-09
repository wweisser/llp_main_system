from dash import Input, Output, State
import gui_panels as gp
# import onque as oq

def tabbar_callback(app):
    @app.callback(
        Output('tab1_btn', 'n_clicks'),
        Output('tab2_btn', 'n_clicks'),
        Output('tab3_btn', 'n_clicks'),
        Output('tab4_btn', 'n_clicks'),
        Output('tab5_btn', 'n_clicks'),
        Output('tab6_btn', 'n_clicks'),
        Output('layouts', 'children'),
        Input('tab1_btn', 'n_clicks'),
        Input('tab2_btn', 'n_clicks'),
        Input('tab3_btn', 'n_clicks'),
        Input('tab4_btn', 'n_clicks'),
        Input('tab5_btn', 'n_clicks'),
        Input('tab6_btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def page_setter(btn1, btn2, btn3, btn4, btn5, btn6):
        if btn1:
            page = gp.plots_page()
        elif btn2:
            page = gp.perfusion_page()
        elif btn3:
            page = gp.metabolics_page()
        elif btn4:
            page = gp.respiratory_page()
        elif btn5:
            page = gp.acive_page()
        else:
            page = gp.conn_page()
        return 0, 0, 0, 0, 0, 0, page


