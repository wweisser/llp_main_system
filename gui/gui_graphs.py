from dash import dcc, html
import plotly.express as px

def create_graph(id, class_name):
    fig = px.scatter(x="sepal_width", y="sepal_length")
    fig.update
    return(
        html.Div([
            dcc.Graph(figure=fig)
        ], id=id, className=class_name )
    )

def create_graph():
    return(
        html.Div([
            create_graph('upper_graph', 'main_pannel_graph'),
            create_graph('middle_graph', 'main_pannel_graph'),
            create_graph('lower_graph', 'main_pannel_graph'),
        ])
    )