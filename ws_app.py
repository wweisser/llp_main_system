from dash import Dash, html, dcc, Output, Input

# Dash-App erstellen
app = Dash(__name__)

# Layout mit Input und Output
app.layout = html.Div([
    html.H1("Tailscale Dash Test"),
    dcc.Input(id="my-input", type="text", placeholder="Text eingeben"),
    html.Div(id="my-output", style={"marginTop": "20px", "fontSize": "20px"})
])

# Callback
@app.callback(
    Output("my-output", "children"),
    Input("my-input", "value")
)
def update_output(value):
    if value:
        return f"Du hast eingegeben: {value}"
    return "Bitte Text eingeben"

# Server starten
if __name__ == "__main__":
    # Auf allen Interfaces lauschen, Debug False
    app.run(host="0.0.0.0", port=8050, debug=False)