from dash import Input, Output, State
import gui_panels as gp
import gui_utils as gu
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
    
    @app.callback(
        Output('note_mdl', 'hidden'),
        Input('note_mdl_btn', 'n_clicks'),
        State('note_mdl', 'hidden'),
        prevent_initial_call=True
    )
    def open_note_mdl(btn, hidden):
        print('hidden: ', hidden)
        if hidden:
            print('note mdl open')
            return False
        else:
            print('note mdl close')
            return True
        
    @app.callback(
        Output('active_mdl', 'hidden'),
        Input('active_mdl_btn', 'n_clicks'),
        State('active_mdl', 'hidden'),
        prevent_initial_call=True
    )
    def open_note_mdl(btn, hidden):
        print('hidden: ', hidden)
        if hidden:
            print('note mdl open')
            return False
        else:
            print('note mdl close')
            return True
    
    @app.callback(
        Output('postbox', 'data', allow_duplicate=True),
        Output('note_input', 'value'),
        Input('enter_note_btn', 'n_clicks'),
        State('note_input', 'value'),
        prevent_initial_call=True
    )
    def enter_note(btn, note):
        if note:
            item = gu.create_postbox_item('entry_request', 'note', note)
            return item, ""
        else:
            return None, ""

    @app.callback(
        Output('note_h1', 'value', allow_duplicate=True),
        Input('state_data_store', 'data'),
        prevent_initial_call=True
    )
    def enter_note(sys_state):
        return sys_state['data']['notes']

    # #automaticaly scrolls the note modal all the way down
    # app.clientside_callback(
    # """
    # function(value) {
    #     const ta = document.getElementById("note_h1");
    #     if (ta) {
    #         ta.scrollTop = ta.scrollHeight;
    #     }
    #     return value;
    # }
    # """,
    # Output("note_h1", "value", allow_duplicate=True),
    # Input("note_h1", "value"),
    # prevent_initial_call=True
    # )
