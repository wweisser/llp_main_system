from dash import dash, dcc, html, Input, Output, State, callback 
import plotly.express as px

mdl_app = dash.Dash(__name__)

def case_manager_mdl():
    return(html.Div([
        html.Span("Please select case number", id="case_mgr_header"),
        dcc.Dropdown(id='cm_dropdown', options=[], clearable=True, persistence=True, placeholder="Select Case Number", className="cm_drpdwn"),
        html.Div([
            html.Button("New Case", id="cm_new_case_button",className="case_mgr_btn"),
            html.Button("Start Case", id="start_case",className="case_mgr_btn"),
            html.Button("Confirm", id="cm_confirm_btn", className="case_mgr_btn"),
            html.Button("Close", id="cm_close_btn",className="case_mgr_btn"),
            html.Button("Start Perfsuion", id="start_case_btn",className="case_mgr_btn"),
            html.Button("default", id="cm_close_btn",className="case_mgr_btn"),

            ], className="case_mgr_mdl_lower"),
        ], className="case_mgr_mdl", id="case_mgr_mdl", hidden=True))

def new_case_mdl():
    return(html.Div([
        html.Div([
            html.Span("Please enter new case number", id="new_case_h1"),
            dcc.Input(id='ncm_input', placeholder="Enter new case number and confirm", className="ncm_input_style"),
            html.Div([
                html.Button("Create New Case", id="ncm_confirm_btn", className="case_mgr_btn"),
                html.Button("Close", id="ncm_close_btn", className="case_mgr_btn"),
            ])
            ], className="new_case_mdl")
        ], id="new_case_mld", hidden=True)
    )

def note_mdl():
    print('\n text mdl was created \n')
    return(html.Div([
        html.Div(children="No Notes listed", id="new_case_h1", className="note_mdl_notes"),
        dcc.Input(id='note_input', placeholder="Note"),
        html.Div([
            html.Button("Enter Note", id="enter_note_btn", className="case_mgr_btn"),
        ]),
        ],  id="note_mdl", className="note_mdl", hidden=True)
    )

def active_mdl():
    print('\n text mdl was created \n')
    return(html.Div([
        # html.Div(children="active elements", id="new_case_h1", className="note_mdl_notes"),
        ],  id="active_mdl", className="active_mdl", hidden=True)
    )

def case_manager_modal():
    return(
        html.Div([
            case_manager_mdl(),
            new_case_mdl(),
            # paramtr_modal(),
        ])
    )

# mit callback auf button implementieren
def paramtr_modal():
    return html.Div([
        html.Div([
            html.H3("---", id="paramtr_mdl_header", className="Paramtr_mdl_header")
            ]),
        html.Div([
            html.Div([
                html.Button("---", id="upper_boundary",className="ha", style={"fontSize": "30px", "color": "red", "text-align": "left"}),
                html.Span("400", id="paramtr_mdl_val", style={"fontSize": "70px", "color": "green", "margin-top": "25px", "text-align": "left"}),
                html.Button("---", id="lower_boundary",  className="ha", style={"fontSize": "30px", "color": "red", "text-align": "left"}),
                html.Span(" "),
                ], className="paramtr_mdl_value"),
            html.Div([
                html.Button("⭡", className="ha", style={"fontSize": "40px"}),
                html.Button("⭣", className="ha", style={"fontSize": "40px"}),
                html.Button("🔕", className="ha", style={"fontSize": "20px"}),
                ], className="paramtr_mdl_up_down")
            ], className="paramtr_mdl_panel"),
        html.Button("Close", id="paramtr_mdl_close", className="ha", style={"border-radius": "10px", "padding": "0", "width": "300px", "height": "45px"})
    ], className="paramtr_mdl", id="paramtr_mld_id", style={"display": "none"})

mdl_app.layout = note_mdl()

if __name__ == '__main__':
    mdl_app.run(debug=True)