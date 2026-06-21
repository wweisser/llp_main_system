from dash import html, dcc
import gui_graphs as gg

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

def value_entry_element(val: str):
    return(html.Div([
        dcc.Input(id=f'{val}_entry_field', placeholder=f"enter {val} value", className='bga_entry_field'),
        html.Button(id=f'{val}_entry_btn', children='Store', className='bga_entry_btn'),
    ], className='bga_entry_element'))

def effector_module():
    return(html.Div([
        ], className="effector_module")
    )

def permanent_panel():
    return(html.Div([
        paramtr_btn_1('art_flow_btn', 'Arterial Flow', '---', '    ml/h', 'art_flow', 'meta', 90),
        paramtr_btn_1('art_pressure_btn', 'Arterial Pressure: ', '---', '  mmHg', 'art_pressure', 'meta', 90),
        paramtr_btn_1('ven_flow_btn', 'Portal Vene Flow: ', '---', ' ml/h', 'ven_flow', 'meta', 90),
        paramtr_btn_1('ven_pressure_btn', 'Portal Vene Pressure: ', '---', 'mmHg:', 'ven_pressure', 'meta', 90),
        paramtr_btn_1('return_temp_btn', 'Return Tmp:    ', '---', '    °C', 'return_temp', 'meta', 100),
        paramtr_btn_1('ven_art_rel_btn', 'Flow A:V:    ', '---:---', '', 'ven_art_rel', 'meta', 100),
        ], id='permanent_panel', className="side_panel_II", hidden=False)
    )

def data_panel():
    return(html.Div([
            html.Div([
            paramtr_btn_1('download_mdl_btn', 'Download', '', '', '', 'ha', 90),
            drop_down_bar({'dummy': 'dummy'}, 'case_number_drop_down', 'case Number'),
            drop_down_bar({'dummy': 'dummy'}, 'chart_2', 'Graph 2'),
            drop_down_bar({'dummy': 'dummy'}, 'chart_3', 'Graph 3'),
            drop_down_bar({'dummy': 'dummy'}, 'chart_4', 'Graph 5'),
            drop_down_bar({'dummy': 'dummy'}, 'data_export', 'Export to Excel'),
            ], className="side_panel_I"),
            gg.create_plot_graph()
        ], id='data_panel', className="hide")
    )

def perfusion_panel():
    return(html.Div([
        html.Div([
            html.Div([
                paramtr_btn_1('art_ph_btn', 'Art pH:   ', '---', '', 'art_ph', 'ha', 100),
                paramtr_btn_1('art_pO2_btn', 'Art pO2: ', '---', ' mmHgh', 'art_po2', 'ha', 90),
                paramtr_btn_1('art_pCO2_btn', 'Art pCO2:    ', '---', ' mmHg', 'art_pco2', 'ha', 100),
                paramtr_btn_1('so2_btn', 'Art SO2:    ', '---', '    %', 'so2', 'ha', 90),
                paramtr_btn_1('art_vr_btn', 'Art VR:    ', '---', '    mmHg/ml/min', 'art_vr', 'ha', 100),
                paramtr_btn_1('art_temp_btn', 'Art Tmp:    ', '---', '    °C', 'art_temp', 'ha', 100),
            ], className="side_panel_I_top"),
            html.Div([
                paramtr_btn_1('ven_ph_btn', 'Ven pH:   ', '---', '', 'ven_ph', 'ven', 100),
                paramtr_btn_1('ven_po2_btn', 'Ven pO2: ', '---', 'mmHg:', 'ven_po2', 'ven', 100),
                paramtr_btn_1('ven_pco2_btn', 'Ven pCO2:    ', '---', 'mmHg:', 'ven_pco2', 'ven', 100),
                paramtr_btn_1('cso2_btn', 'Ven SO2:    ', '---', '    %', 'cso2', 'ven', 90),
                paramtr_btn_1('ven_vr_btn', 'Ven VR:    ', '---', '    mmHg/ml/min', 'ven_vr', 'ven', 100),
                paramtr_btn_1('ven_temp_btn', 'Ven Tmp:    ', '---', '    °C', 'ven_temp', 'ven', 100),
            ], className="side_panel_I_middle"),
            html.Div([
                paramtr_btn_1('do2_btn', 'DO2:    ', '---', 'ml/min', 'do2', 'meta', 100),
                paramtr_btn_1('vo2_btn', 'VO2:    ', '---', 'ml/min', 'vo2', 'meta', 100),
                paramtr_btn_1('base_btn', 'Base:    ', '---', '', 'base', 'meta', 100),
                paramtr_btn_1('ox_index_btn', 'Oxygenation Index:    ', '---', '    %', 'ox_index', 'meta', 100),
                paramtr_btn_1('decarb_index_btn', 'Decarb Index:    ', '---', '    ml/min/mmHg', 'decab_index', 'meta', 100),
                paramtr_btn_1('hco3_btn', 'HCO3:    ', '---', '    mg/dl', 'hco3', 'meta', 100),
                paramtr_btn_1('lactate_btn', 'Lactate:    ', '---', '    mmol/L', 'lactate', 'meta', 100),
                paramtr_btn_1('k_btn', 'Potasium:    ', '---', '    mmol/L', 'k', 'meta', 100),
                paramtr_btn_1('glucose_btn', 'Glucose:    ', '---', '    mmol/L', 'glucose', 'meta', 100),
            ], className="side_panel_I_bottom"),
        ], className="side_panel_I"),
        gg.create_graph_panel("flow_graph", "pressure_graph", "hb_hct_graph"),
        ], id='perfusion_panel', className="left_controlled_page")
    )

def ph_panel():
    return(html.Div([
        html.Div([
        ], className="side_panel_I"),
        gg.create_graph_panel("ph_graph", "k_lact_graph", "base_gluc_graph"),
        ], id='ph_panel', className="hide")
    )

def respiratory_panel():
    return(html.Div([
        html.Div([
        ], className="side_panel_I"),
        gg.create_graph_panel("do2_graph", "hb_graph", "po2_graph"),
        ], id='respiratory_panel', className="hide")
    )

def bga_entry_panel():
    return(html.Div([
        html.Div([
            value_entry_element('na'),
            value_entry_element('glucose'),
            value_entry_element('lactate'),
            value_entry_element('ca'),
            value_entry_element('cl'),
            value_entry_element('hb'),
            value_entry_element('hct'),
            value_entry_element('met_hb'),
            value_entry_element('fco'),
            value_entry_element('fhhb'),
            value_entry_element('fohb'),
            value_entry_element('bilirubin'),
            value_entry_element('bile_ph'),
            value_entry_element('bile_glucose'),
            value_entry_element('bile_hco3'),
            value_entry_element('bile_bilirubin'),
        ], className="side_panel_I"),
        ], id='bga_entry_panel', className="hide", hidden=True)
    )



def tab_bar():
    return(html.Div([
        cntrl_btn('case_manager', 'Perfusion Start: ', 'start_time', 'Clock Time:', 'clock_time', 'Case ID: ', 'case_id','meta'),
        cntrl_btn('active_mdl_btn', '---', 'perfusion_mode', '---', 'perfuison_time', '', '','meta'),
        paramtr_btn_1('tab1_btn', 'Plots', '', '','tab1', 'tabbar_btn', 90),
        paramtr_btn_1('tab2_btn', 'Perfusion', '', '','tab2', 'tabbar_btn', 90),
        paramtr_btn_1('tab3_btn', 'Metabolics', '', '', 'tab3', 'tabbar_btn', 90),
        paramtr_btn_1('tab4_btn', 'Respiration', '', '', 'tab4', 'tabbar_btn', 90),
        paramtr_btn_1('tab5_btn', 'Active', '', '', 'tab5', 'tabbar_btn', 90),
        paramtr_btn_1('tab6_btn', 'Connections', '', '', 'tab6', 'tabbar_btn', 90),
        cntrl_btn('note_mdl_btn',  'Note', 'cntrl_cm_lower', '', 'tab7', '', 'note_lower', 'meta'),
        cntrl_btn('alarm_btn',  'Mute Alarm', 'mute_btn', '', 'tab8', '', 'alarm_lower', 'meta'),
        ], id='tab_bar', className="tabbar")
    )

def drop_down_bar(options: dict, id: str, name: 'str'):
    layout = html.Div([
                html.Div(children=name),
                dcc.Dropdown(options=options, value='Select', id=id, multi=True, closeOnSelect=False, searchable=True, className='ha'),
            ])
    return layout


def create_pages():
    return(html.Div([
        data_panel(),
        perfusion_panel(),
        ph_panel(),
        respiratory_panel(),
        bga_entry_panel(),
        permanent_panel(),
 
    ], id="layouts", className="layouts_style")
    )

