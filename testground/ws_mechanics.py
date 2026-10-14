import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

# Funktion, die die Tacho-Grafik generiert
def erstelle_tacho(aktueller_wert=20):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aktueller_wert,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Geschwindigkeit (km/h)", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "#1f77b4"}, # Farbe der Nadel / des Balkens
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            # Hier kannst du wie zuvor Farbbereiche definieren!
            'steps': [
                {'range': [0, 50], 'color': '#e8f5e9'},   # Grün (Sicher)
                {'range': [50, 80], 'color': '#fff9c4'},  # Gelb (Warnung)
                {'range': [80, 100], 'color': '#ffcdd2'}  # Rot (Gefahr)
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Transparenter Hintergrund
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        # 'v' wurde entfernt, da 't' (top) und 'b' (bottom) schon reichen
        margin=dict(l=30, r=30, t=40, b=30) 
    )

app.layout = html.Div([
    html.Div(
        dcc.Graph(
            id="tacho-graph", 
            figure=erstelle_tacho(20),
            # Deaktiviert das lästige Plotly-Menü beim Hovern für einen cleanen Widget-Look
            config={'displayModeBar': False} 
        ),
        style={"width": "450px", "margin": "auto"}
    ),
    html.Div(id="tacho-info", style={"textAlign": "center", "fontSize": "18px", "marginTop": "10px"})
])

@app.callback(
    Output("tacho-graph", "figure"),
    Output("tacho-info", "children"),
    Input("tacho-graph", "clickData") # Reagiert auf Klicks direkt in der Grafik
)
def tacho_geklickt(click_data):
    # Wenn noch kein Klick passiert ist, zeige den Startwert 20
    if click_data is None:
        return erstelle_tacho(20), "Klicke auf den Tacho, um den Wert zu ändern."
    
    # Plotly ist schlau: Es gibt uns direkt den mathematischen Wert des angeklickten Punkts!
    neuer_wert = click_data['points'][0]['v']
    
    # Wir runden den Wert für eine saubere Anzeige
    neuer_wert_gerundet = round(neuer_wert, 1)
    
    # Tacho mit neuem Wert neu zeichnen
    neue_figur = erstelle_tacho(neuer_wert_gerundet)
    text = f"Gesetzter Wert: {neuer_wert_gerundet} km/h"
    
    return neue_figur, text

if __name__ == "__main__":
    app.run(debug=True)