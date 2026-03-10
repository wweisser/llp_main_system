from dash import dash, html, dcc
from dash_extensions import WebSocket
import gui_utils as gu
import gui_panels as gp
import gui_modals as gm
import gui_callbacks as gc
import gui_active_callbacks as ga
import gui_graphs as gg
import gui_case_management as gcm
import gui_parameter_callbacks as gpc


def create_layouts():
    return(html.Div([
        gp.create_pages(),
        gp.tab_bar(),
    ]))
def create_modals():
    return(html.Div([
        gm.case_manager_mdl(),
        gm.new_case_mdl(),
        gm.note_mdl(),
        gm.create_active_mdl()
    ]))

def create_callbacks(app):
    return(html.Div([
        gc.tabbar_callback(app),
        gcm.case_manager_callbacks(app, 'case_manager')
    ]))

def create_communication(app):
    print('Websocket was created')
    return(html.Div([
        # dcc.Store(id="pbox"),
        gu.create_msg_distribution(),
        # WebSocket(url="ws://127.0.0.1:5000/ws", id="ws"),
        WebSocket(url="/ws", id="ws")
    ]))

def create_com_callbacks(app):
    return(html.Div([
        gu.gui_ws_recv(app),
        gu.gui_ws_send(app),
        ga.create_active_callbacks(app),
        # gd.distribute_state(app),
        gpc.state_to_gui(app)
    ]))


def create_gui(app):
    return(html.Div([
        create_communication(app),
        gm.create_modals(),
        # create_modals(),
        create_layouts(),
    ], className="background"))

def create_app():
    print("gui ausgelöst")
    # gui_app = dash.Dash(__name__, requests_pathname_prefix='/dashboard1/')
    gui_app = dash.Dash(__name__)
    gui_app.layout = create_gui(gui_app)
    create_com_callbacks(gui_app)
    create_callbacks(gui_app)

    return gui_app

app = create_app()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

