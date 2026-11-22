import gui_panels as gp
from dash import dash, dcc, html, Input, Output, State, callback 
import plotly.express as px

mdl_app = dash.Dash(__name__)

def case_manager_mdl():
    return(html.Div([
        html.Span("Please select case number", id="case_mgr_header"),
        dcc.Dropdown(id='case_id_dropdown', options=[], clearable=True, multi=False, persistence=True, placeholder="Select Case Number", className="cm_drpdwn"),
        html.Div([
            html.Button("New Case", id="cm_new_case_btn",className="case_mgr_btn"),
            html.Button("HOPE", id="hope_btn",className="case_mgr_btn"),
            html.Button("Confirm", id="cm_confirm_btn", className="case_mgr_btn"),
            html.Button("COR", id="cor_btn",className="case_mgr_btn"),
            html.Button("Start Perfusion", id="start_case_btn",className="case_mgr_btn"),
            html.Button("NMP", id="nmp_btn",className="case_mgr_btn"),
            ], className="case_mgr_mdl_lower"),
        ], className="hide", id="case_mgr_mdl"))

def new_case_mdl():
    return(html.Div([
            html.Span("Please enter new case number", id="new_case_h1"),
            dcc.Input(id='ncm_input', placeholder="Enter new case number here", className="ncm_input_style"),
            html.Div([
                html.Button("Create New Case", id="ncm_confirm_btn", className="case_mgr_btn"),
                html.Button("Close", id="ncm_close_btn", className="case_mgr_btn", n_clicks=0),
            ]),
        ], id="new_case_mld", className="hide")
    )

def value_controll_module(val: str):
    return(html.Div([
        html.Div([
            html.Span(id=val, children="---"),
            html.Div([
                html.Button(id="up"),
                html.Button(id="down")

            ])
        ])

    ], className="default"))


def gbm_panel():
    marks_set_po2 = {80: '80', 100: '100', 120: '120', 140: '140', 160: '160'}
    marks_set_pco2 = {20: '20' , 30: '30', 40: '40', 50: '50', 60: '60'}
    marks_gas_fio2 = {21: '21', 40: '40', 60: '60', 80: '80', 100: '100'}
    marks_gas_flow = {0: '0', 200: '200', 400: '400', 600: '600', 800: '800', 1000: '1000'}

    return(html.Div([
        html.Div([
            html.Div([
                gp.paramtr_btn_1('air_flow_btn', 'air flow', '0', 'ml/min', 'air_flow','meta', 70),
                gp.paramtr_btn_1('o2_flow_btn', 'O2 flow', '0', 'ml/min', 'oxygen_flow','meta', 70),
                gp.paramtr_btn_1('set_po2_btn', 'set po2', '0', 'mmHg', 'set_po2','meta', 70),
                gp.paramtr_btn_1('set_pco2_btn', 'set pco2', '0', 'mmHg', 'set_pco2','meta', 70),
                html.Fieldset([
                    dcc.Slider(id='set_po2_slider', min=80, max=160, step=1, value=100, marks=marks_set_po2, vertical=True, verticalHeight=180, dots=False, disabled=True, className='input_bar'),
                    ], id='set_po2_slider_area', className='slider_area', disabled=True),
                html.Fieldset([
                    dcc.Slider(id='set_pco2_slider', min=20, max=60, step=1, value=45, marks=marks_set_pco2, vertical=True, verticalHeight=180, dots=False, disabled=True, className='input_bar'),
                    ], id='set_pco2_slider_area', className='slider_area', disabled=True),
                ], id="ventilaton_setings", className="ventilaton_setings"),
            html.Div([
                gp.paramtr_btn_1('fio2_btn', 'FiO2', '0', '%', 'fio2','meta', 70),
                gp.paramtr_btn_1('output_gas_btn', 'gas flow', '0', 'ml/min', 'gas_flow','meta', 70),
                gp.paramtr_btn_1('set_fio2_btn', 'set fiO2', '0', '%', 'set_fio2','meta', 70),
                gp.paramtr_btn_1('set_gas_flow_btn', 'set gas flow', '0', 'mmHg', 'set_gas_flow','meta', 70),
                html.Fieldset([
                    dcc.Slider(id='set_fio2_slider', min=21, max=100, step=1, value=21, marks=marks_gas_fio2, vertical=True, verticalHeight=180, dots=False, disabled=True, className='input_bar'),
                    ], id='set_fio2_slider_area', className='slider_area', disabled=True),
                html.Fieldset([
                    dcc.Slider(id='set_gas_flow_slider', min=0, max=1000, step=1, value=100, marks=marks_gas_flow, vertical=True, verticalHeight=180, dots=False, disabled=True, className='input_bar'),
                    ], id='set_gas_flow_slider_area', className='slider_area', disabled=True),
                ], id="gas_flow_setings", className="ventilaton_setings"),
            ], className='gbm_settings'),
        html.Button("AUTO", id="gbm_align_btn", className='align_btn_off'),
        ], id="gbm_panel", className="gbm_panel")
    )

def create_active_mdl():
    print('\ncomunication panel\n')
    return(html.Div([
        gbm_panel(),
        ], id='com_panel', className='hide')
    )

def create_download_mdl():
    return(html.Div([
        html.Div([
            
            ], className="download_mdl_data_type_select"),
        # html.Div([
        #     ], className="download_btn"),
        html.Button("Download Data", id="download_btn",className="download_btn"),
        ], id='download_mdl', className="hide")
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
        create_active_mdl(),
        create_download_mdl(),
    ]))

# mdl_app.layout = note_mdl()

if __name__ == '__main__':
    mdl_app.run(debug=True)