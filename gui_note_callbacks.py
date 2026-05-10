from dash import Input, Output, html, State, no_update
from dash.exceptions import PreventUpdate
import gui_utils as gu
import gui_case_management as gcm
import gui_panels as gp

def create_note_callbacks(app):
#send input to backend
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
        Output("postbox", "data", allow_duplicate=True),
        Input('enter_note_btn', 'n_clicks'),
        State('note_input', 'value'),
        prevent_initial_call=True
    )
    def send_note_entry(input_btn, input_value):
        send_item = gu.create_postbox_item('archive', 'note_entry', input_value)
        return send_item

    app.clientside_callback(
        """
        function(value) {
            setTimeout(function() {
                var el = document.getElementById('note_h1');
                if (el) el.scrollTop = el.scrollHeight;
            }, 50);
            return null;
        }
        """,
        Output("_scroll_dummy", "children"),
        Input("note_h1", "value"),
    )
    
#put note item to gui
    @app.callback(
        Output('note_h1', 'value'),
        Input('note_data_store', 'data'),
        State('note_h1', 'id'),
        prevent_initial_call=True
    )
    def note_to_gui(msg, note_id):
        if note_id is None:
            raise PreventUpdate
        if isinstance(msg, dict) and msg['id'] == 'notes':
            print(f'note_to_gui -> {msg['time']}')
            # print(f'note_to_gui -> {msg['data']}')
            return msg['data']
        return no_update

#take note stack form graph update

#merge state and stack notes
