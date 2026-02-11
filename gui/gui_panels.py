from dash import html
import plotly.express as px
import gui_modals as gm

# alle controll button damit belegen
def cntrl_btn(button_id, upper_text, upper_text_id, middle_text, middle_text_id, lower_text, lower_text_id, class_name):
    return html.Button(
        html.Span([
            html.Span(upper_text, id=upper_text_id, style={"fontSize": "100%", "display": "block", "textAlign": "left"}),
            html.Span(middle_text, id=middle_text_id, style={"fontSize": "100%", "display": "block", "textAlign": "left"}),
            html.Span(lower_text, id=lower_text_id, style={"fontSize": "100%", "display": "block", "textAlign": "left"}),
                ]),
        className=class_name,
        id=button_id
    )
# alle parameter button damit belegen
def paramtr_btn_1(button_id, top_text, middle_text, bottom_text, text_id, class_name, size):
    big_size = size * 2.2
    return html.Button(
        html.Span([
            html.Span(top_text, style={"fontSize": f"{size}%", "display": "block"}),
            html.Label(middle_text, id=text_id, style={"display": "inline-block", "fontSize": f"{big_size}%", "width": "60px"}),
            html.Span(bottom_text, style={"fontSize": f"{size}%"}),
        ]), 
        id=button_id,
        className=class_name
    )

def paramtr_btn_2(button_id, top_text, middle_text, bottom_text, text_id, class_name, size):
    big_size = size * 2.2
    return html.Button(
        html.Span([
            html.Span(top_text, style={"fontSize": f"{size}%"}),
            html.Label(middle_text, id=text_id, style={"display": "inline-block", "fontSize": f"{big_size}%", "width": "45px"}),
            html.Span(bottom_text, style={"fontSize": f"{size}%"}),
        ]), 
        id=button_id,
        className=class_name
    )

def create_prb(id_prg):
    return (html.Div([
        html.Div(id="progress-inner")], 
        style={"width": "100%", "backgroundColor": "#a2a2a1", "height": "20px", "overflow": "hidden"},
        id=id_prg)
        )

def module():
    return(html.Div([
        html.Div(id="dummy", children="dummy")
        ], id="module", className="modul_lyt")
    )

def create_med_module(id_med_module):
    return(html.Div([
        html.Div([
            html.Span(children='Med', id=f'{id_med_module}_med', style={"fontSize": "180%", "width": "20%", "height": "10%", "display": "inline-block"}),
            html.Span([
                html.Span(children='Vol   ', id=f'{id_med_module}_rate',  style={"fontSize": "180%"}),
                html.Span(children='Unit', id=f'{id_med_module}_unit', style={"fontSize": "80%"})
                ])
            ], className='ha'),  
        html.Div([
            create_prb("id_prg"),
            html.Button("Stop", id=f"{id_med_module}_stop", className="stop_button", style={"height": "40px", "width": "100px"}),
            html.Button("Bolus", id=f"{id_med_module}_bolus", className="bolus_button", style={"height": "40px", "width": "100px"})
            ]),
        ], id=id_med_module)
    )

def effector_module():
    return(html.Div([
        ], className="effector_module")
    )

# def top_line():
#     return(html.Div([
#         cntrl_btn('perfusion_timer', 'Start Case: ', 'start_time', 'Perfusion Time:', 'perfusion_time', 'ha'),
#         cntrl_btn('mode_timer', 'Start mode: ', 'start_mode', 'Mode Time:', 'mode_time', 'ha'),
#         cntrl_btn('case_manager', 'Case ID: ', 'cntrl_cm_upper', '', 'cntrl_cm_lower', 'ha'),
#         ],className="top_line")
#     )

def permanent_panel():
    return(html.Div([
        paramtr_btn_1('art_flow_btn', 'Arterial Flow', '---', '    ml/h', 'art_flow', 'ha', 90),
        paramtr_btn_1('art_pressure_btn', 'Arterial Pressure: ', '---', '  mmHg', 'art_pressure', 'ha', 90),
        paramtr_btn_1('ven_flow_btn', 'Portal Vene Flow: ', '---', ' ml/h', 'ven_flow', 'ha', 90),
        paramtr_btn_1('ven_pressure_btn', 'Portal Vene Pressure: ', '---', 'mmHg:', 'ven_pressure', 'ha', 90),
        paramtr_btn_1('cSO2_btn', 'Art SO2:    ', '---', '    %', 'cso2', 'ha', 90),
        paramtr_btn_1('art_pO2_btn', 'Art pO2: ', '---', ' mmHgh', 'art_po2', 'ha', 90),
        ],className="side_panel_II")
    )

def perf_stat_panel():
    return(html.Div([
        paramtr_btn_1('art_vr_btn', 'Art VR:    ', '---', '    mmHg/ml/min', 'art_vr', 'ha', 100),
        paramtr_btn_1('art_temp_btn', 'Art Tmp:    ', '---', '    °C', 'art_temp', 'ha', 100),
        paramtr_btn_1('ven_vr_btn', 'Ven VR:    ', '---', '    mmHg/ml/min', 'ven_vr', 'ha', 100),
        paramtr_btn_1('ven_temp_btn', 'Ven Tmp:    ', '---', '    °C', 'ven_temp', 'ha', 100),
        paramtr_btn_1('return_temp_btn', 'Return Tmp:    ', '---', '    °C', 'return_temp', 'ha', 100),
        paramtr_btn_1('ven_art_rel_btn', 'Flow A:V:    ', '---:---', '', 'ven_art_rel', 'ha', 100),
        ],className="side_panel_I")
    )

def third_panel():
    return(html.Div([
        paramtr_btn_1('art_pH_btn', 'Art pH:   ', '---', '', 'art_ph', 'ha', 80),
        paramtr_btn_1('ven_pH_btn', 'Ven pH:   ', '---', '', 'ven_ph', 'ha', 80),
        paramtr_btn_1('art_pCO2_btn', 'Art pCO2:    ', '---', ' mmHg', 'art_pco2', 'ha', 80),
        paramtr_btn_1('ven_pCO2_btn', 'Ven pCO2:    ', '---', 'mmHg:', 'ven_pco2', 'ha', 80),
        paramtr_btn_1('art_pO2_btn', 'Art pO2: ', '---', ' mmHgh', 'art_po2', 'ha', 80),
        paramtr_btn_1('ven_pO2_btn', 'Ven pO2: ', '---', 'mmHg:', 'ven_po2', 'ha', 80),
        ],className="third_panel")
    )


def side_panel_1():
    return(html.Div([
        paramtr_btn_1('cSO2_btn', 'Art SO2:    ', '---', '    %', 'cSO2', 'ha', 70),
        paramtr_btn_1('SO2_btn', 'Ven SO2:    ', '---', '    %', 'SO2', 'ha', 70),
        paramtr_btn_1('art_pCO2_btn', 'Art pCO2:    ', '---', ' mmHg', 'art_pco2', 'ha', 80),
        paramtr_btn_1('ven_pCO2_btn', 'Ven pCO2:    ', '---', 'mmHg:', 'ven_pco2', 'ha', 80),
        paramtr_btn_1('art_pO2_btn', 'Art pO2: ', '---', ' mmHgh', 'art_po2', 'ha', 80),
        paramtr_btn_1('ven_pO2_btn', 'Ven pO2: ', '---', 'mmHg:', 'ven_po2', 'ha', 80)
        ],className="side_panel_I")
    )

def ph_panel():
    return(html.Div([
        paramtr_btn_1('art_pH_btn', 'Art pH:   ', '---', '', 'art_ph', 'ha', 100),
        paramtr_btn_1('ven_pH_btn', 'Ven pH:   ', '---', '', 'ven_ph', 'ha', 100),
        paramtr_btn_1('Base_btn', 'Base:    ', '---', '', 'base', 'ha', 100),
        paramtr_btn_1('lactate_btn', 'Lactate:    ', '---', '    mmol/L', 'lactate', 'ha', 100),
        paramtr_btn_1('K_btn', 'Potasium:    ', '---', '    mmol/L', 'k', 'ha', 100),
        paramtr_btn_1('glucose_btn', 'Glucose:    ', '---', '    mmol/L', 'glucose', 'ha', 100),
        ],className="side_panel_I")
    )

def respiratory_panel():
    return(html.Div([
        paramtr_btn_1('DO2_btn', 'DO2:    ', '---', 'ml/min', 'do2', 'ha', 100),
        paramtr_btn_1('VO2_btn', 'VO2:    ', '---', 'ml/min', 'vo2', 'ha', 100),
        paramtr_btn_1('HB_btn', 'HB:    ', '---', '    mg/dl', 'hb', 'ha', 100),
        paramtr_btn_1('art_pCO2_btn', 'Art pCO2:    ', '---', ' mmHg', 'art_pco2', 'ha', 100),
        paramtr_btn_1('ven_pO2_btn', 'Ven pO2: ', '---', 'mmHg:', 'ven_po2', 'ha', 100),
        paramtr_btn_1('ven_pCO2_btn', 'Ven pCO2:    ', '---', 'mmHg:', 'ven_pco2', 'ha', 100),

        # paramtr_btn_1('Hct_btn', 'HCT:    ', '---', '', 'Hct', 'ha', 100),
        # paramtr_btn_1('HCO3_btn', 'HCO3:    ', '---', 'mmol/L', 'hco3', 'ha', 100),
        ],className="side_panel_I")
    )

def tab_bar():
    return(html.Div([
        cntrl_btn('case_manager', 'Perfusion Start: ', 'start_time', 'Clock Time:', 'clock_time', 'Case ID: ', 'case_id','ha'),
        cntrl_btn('active_mdl_btn', '---', 'perfusion_mode', '---', 'perfuison_time', '', '','ha'),
        paramtr_btn_1('tab1_btn', 'Plots', '', '','tab1', 'tabbar_btn', 90),
        paramtr_btn_1('tab2_btn', 'Perfusion', '', '','tab2', 'tabbar_btn', 90),
        paramtr_btn_1('tab3_btn', 'Metabolics', '', '', 'tab3', 'tabbar_btn', 90),
        paramtr_btn_1('tab4_btn', 'Respiration', '', '', 'tab4', 'tabbar_btn', 90),
        paramtr_btn_1('tab5_btn', 'Active', '', '', 'tab5', 'tabbar_btn', 90),
        paramtr_btn_1('tab6_btn', 'Connections', '', '', 'tab6', 'tabbar_btn', 90),
        cntrl_btn('note_mdl_btn',  'Note', 'cntrl_cm_lower', '', 'defaultI', '', 'defaultII', 'ha'),
        cntrl_btn('alarm_btn',  'Mute Alarm', 'cntrl_cm_lower', '', 'defaultI', '', 'defaultII', 'ha'),
        ], className="tabbar")
    )

def plots_page():
    return(html.Div([
        permanent_panel(),
        module()
    ], className='plots_page_syle'))

def perfusion_page():
    return(html.Div([
        permanent_panel(),
        perf_stat_panel(),
    ], className='main_page_syle'))

def metabolics_page():
    return(html.Div([
        permanent_panel(),
        ph_panel()
    ], className='config_page_syle', hidden=False))

def respiratory_page():
    return(html.Div([
        permanent_panel(),
        respiratory_panel()
    ], className='cloud_page_syle', hidden=False))

def acive_page():
    return(html.Div([
        permanent_panel(),
    ], className='active_page_syle', hidden=False))

def conn_page():
    return(html.Div([
        permanent_panel(),
    ], className='conn_page_syle', hidden=False))


def create_pages():
    return(html.Div([
        plots_page(),
        perfusion_page(),
        metabolics_page(),
        respiratory_page(),
        acive_page(),
        conn_page(),
    ], id="layouts", className="layouts_style")
    )


