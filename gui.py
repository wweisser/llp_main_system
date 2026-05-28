from dash import dash, html, dcc, Input, Output
from dash_extensions import WebSocket
from flask import request
import gui_utils as gu
import gui_panels as gp
import gui_modals as gm
import gui_callbacks as gc
import gui_active_callbacks as ga
import gui_graphs as gg
import gui_case_management as gcm
import gui_parameter_callbacks as gpc
import gui_graph_callbacks as ggc
import gui_note_callbacks as gnc
import gui_download_callbacks as gdc


def create_layouts():
    return(html.Div([
        gp.create_pages(),
        # gg.create_center_panels(),
        gp.tab_bar(),
    ]))
def create_modals():
    return(html.Div([
        gm.case_manager_mdl(),
        gm.new_case_mdl(),
        gm.note_mdl(),
        gm.create_active_mdl()
    ]))

#HIER EVTL DICT EINFÜHREN, WO ALLE STRUKTUREN VERZEICHNET SIND

def create_callbacks(app):
    return(html.Div([
        gc.tabbar_callback(app),
        gcm.case_manager_callbacks(app, 'case_manager'),
        # ggc.create_graph_callback_tree(app)
    ]))

def create_communication(app, ts_ip):
    communication = (html.Div([
        dcc.Location(id='location'),
        gu.create_msg_distribution(),
        WebSocket(id="ws"),
        gu.gui_ws_recv(app),
        gu.gui_ws_send(app),
    ]))
    @app.callback(
        Output('ws', 'url'),
        Input('location', 'href')
    )
    def set_ws_url(href):
        print(f'create_communication -> url : {href}')

        if href or href == 'http://127.0.0.1:8050/':
            print(f'create_communication -> connection to localhost created')
            return f"ws://localhost:8000/ws"
        else:
            print(f'create_communication -> connection to client in tailnet created')
            return f"ws://{ts_ip}:8000/ws"
    
    print('Websocket was created')
    return communication

def create_comunication_callbacks(app, graph_list: list):
    return(html.Div([
        ga.create_active_callbacks(app),
        ggc.create_graph_callbacks(app),
        gnc.create_note_callbacks(app),
        gdc.create_active_callbacks(app),

        # ggc.create_graph_callbacks(app, 'graph_data_store', graph_list),
        gpc.state_to_gui(app)
    ]))

def create_gui(app, ts_ip):
    return(html.Div([
        create_communication(app, ts_ip),
        gm.create_modals(),
        # create_modals(),
        create_layouts(),
    ], className="background"))

def create_app(ts_ip):
    graph_list = ["ph_graph", "base_lact_graph", "k_gluc_graph", "do2_vo2_graph", "po2_graph", "pco2_graph", "flow_graph", "pressure_graph", "hb_hct_graph"]
    print("gui ausgelöst")
    gui_app = dash.Dash(__name__)
    gui_app.layout = create_gui(gui_app, ts_ip)
    create_comunication_callbacks(gui_app, graph_list)
    create_callbacks(gui_app)
    # WebSocket-URL dynamisch anhand von window.location setzen
    return gui_app



if __name__ == '__main__':
    tailscale_ip =  '100.94.159.38'
    app = create_app(tailscale_ip)
    app.run(host="127.0.0.1", port=8050, debug=True)

#WS_HOST=100.94.159.38 python gui.py

