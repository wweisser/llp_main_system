import gui_panels as gp
from dash import dash, dcc, html, Input, Output, State, callback 
import plotly.express as px

mdl_app = dash.Dash(__name__)

def case_manager_mdl():
    return(html.Div([
        html.Span("Please select case number", id="case_mgr_header"),
        dcc.Dropdown(id='cm_dropdown', options=[], clearable=True, multi=False, persistence=True, placeholder="Select Case Number", className="cm_drpdwn"),
        html.Div([
            html.Button("New Case", id="cm_new_case_button",className="case_mgr_btn"),
            html.Button("HOPE", id="default_I",className="case_mgr_btn"),
            html.Button("Confirm", id="cm_confirm_btn", className="case_mgr_btn"),
            html.Button("COR", id="cm_close_btn",className="case_mgr_btn"),
            html.Button("Start Perfusion", id="start_case_btn",className="case_mgr_btn"),
            html.Button("NMP", id="stop_case_btn",className="case_mgr_btn"),
            ], className="case_mgr_mdl_lower"),
        ], className="case_mgr_mdl", id="case_mgr_mdl", hidden=True))

def new_case_mdl():
    return(html.Div([
        html.Div([
            html.Span("Please enter new case number", id="new_case_h1"),
            dcc.Input(id='ncm_input', placeholder="Enter new case number here", className="ncm_input_style"),
            html.Div([
                html.Button("Create New Case", id="ncm_confirm_btn", className="case_mgr_btn"),
                html.Button("Close", id="ncm_close_btn", className="case_mgr_btn"),
            ]),
            ], className="new_case_mdl")
        ], id="new_case_mld", hidden=True)
    )

def note_mdl():
    print('\n text mdl was created \n')
    return(html.Div([
        dcc.Textarea(value="No Notes listed", id="note_h1", className="note_mdl_notes", readOnly=True),
        dcc.Input(id='note_input', placeholder="Note"),
        dcc.Store(id='note_store'),
        html.Div([
            html.Button("Enter Note", id="enter_note_btn", className="case_mgr_btn"),
        ]),
        ],  id="note_mdl", className="note_mdl", hidden=True)
    )

def create_active_mdl():
    print('\n Active mdl was created \n')
    marks_set_po2 = {80: '80', 100: '100', 120: '120', 140: '140', 160: '160', 180: '180', 200: '200'}
    marks_set_pco2 = {20: '20' , 30: '30', 40: '40', 50: '50', 60: '60'}
    marks_gas_flow = {0: '0', 400: '400', 800: '800', 800: '1200', 1200: '1400', 1600: '1600', 2000: '2000'}
    return(html.Div([
        html.Div([
            gp.paramtr_btn_1('output_gas_btn', 'Gas Flow', '0', 'ml/min', 'gas_flow','ha', 80),
            gp.paramtr_btn_1('fio2_btn', 'FiO2', '0', '%', 'fio2','ha', 80),
            gp.paramtr_btn_1('set_po2_btn', 'set pO2', '0', 'mmHg', 'set_po2','ha', 80),
            gp.paramtr_btn_1('set_pco2_btn', 'set pCO2', '0', 'mmHg', 'set_pco2','ha', 80),
            dcc.Slider(id='set_po2_slider', min=80, max=200, step=1, value=100, marks=marks_set_po2, vertical=True, verticalHeight=190, dots=False),
            dcc.Slider(id='set_pco2_slider', min=20, max=60, step=1, value=45, marks=marks_set_pco2, vertical=True, verticalHeight=190, dots=False),
            ], id="ventilaton_setings", className="ventilaton_setings"),
        html.Div([
            gp.paramtr_btn_1('air_flow_btn', 'Air Flow', '0', 'ml/min', 'air_flow','ha', 70),
            gp.paramtr_btn_1('o2_flow_btn', 'O2 Flow', '0', 'ml/min', 'o2_flow','ha', 70),
            gp.paramtr_btn_1('set_air_flow_btn', 'set air flow', '0', 'ml/min', 'set_air_flow','ha', 70),
            gp.paramtr_btn_1('set_o2_flow_btn', 'set 02 flow', '0', 'ml/min', 'set_o2_flow','ha', 70),
            dcc.Slider(id='set_air_flow_slider', min=0, max=2000, step=1, value=45, marks=marks_gas_flow, vertical=True, verticalHeight=190, dots=False),
            dcc.Slider(id='set_o2_flow_slider', min=0, max=2000, step=1, value=45, marks=marks_gas_flow, vertical=True, verticalHeight=190, dots=False),
            ], id="gas_flow_setings", className="ventilaton_setings"),
        ], id="active_mdl", className="active_mdl", hidden=True)
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

def create_modals():
    return(html.Div([
        case_manager_mdl(),
        new_case_mdl(),
        note_mdl(),
        create_active_mdl()
    ]))

mdl_app.layout = note_mdl()

if __name__ == '__main__':
    mdl_app.run(debug=True)