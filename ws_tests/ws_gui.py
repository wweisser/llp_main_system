from dash_extensions import WebSocket
from dash_extensions.enrich import DashProxy, Input, Output, dcc, html
import json

# Create example app.
def create_layout():
    return html.Div(
        [
            html.Div(id="message", children="alive"),
            WebSocket(url="ws://127.0.0.1:5000/ws", id="ws"),
        ]
    )

def create_callbacks(app):

    @app.callback(
        Output("message", "children"), 
        Input("ws", "message")
        )
    def send_back(msg):
        print('data received from frontend')
        msg_obj = msg['data']
        data = json.loads(msg_obj)
        return str(data)

def create_gui_app():
    app = DashProxy(prevent_initial_callbacks=True)
    app.layout = create_layout()
    create_callbacks(app)
    app.run(use_reloader=True)

if __name__ == "__main__":
    create_gui_app()