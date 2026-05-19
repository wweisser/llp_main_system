from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go


def update_graph_layout(figure):
    if isinstance(figure, dict):
        figure = go.Figure(figure)
    
    figure.update_layout(
        margin=dict(l=0, r=100, t=0, b=0),
        legend=dict(x=1, y=0.9, xanchor='left', yanchor='top'),
        paper_bgcolor='#00242b',
        plot_bgcolor="#00242b",
        font_color='#ccebfd', 
    )
    figure.update_xaxes(
        tickformat='%H:%M:%S',
        showgrid=False,
    )
    figure.update_yaxes(
        griddash='dot',
        gridwidth=1,
        gridcolor='#005161'
        # tickvals=[0, 10, 25, 50, 100]
    ),
    return figure

def create_graph(id, class_name):
    fig = px.scatter(x=None, y=None)
    fig = update_graph_layout(fig)
    return(
        html.Div([
            dcc.Graph(figure=fig,
            className=class_name,
            id=id)
        ], className= class_name)
    )

def create_graph_panel(upper_graph: str, middle_graph: str, lower_graph: str):
    return(
        html.Div([
            create_graph(upper_graph, 'center_graph'),
            create_graph(middle_graph, 'center_graph'),
            create_graph(lower_graph, 'center_graph'),
        ], className='center_graph_panel')
    )

def create_plot_graph():
    return(
        html.Div([
            create_graph('plot_gaph', 'plot_graph'),
        ])
    )