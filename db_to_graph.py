import onque as oq
import db_utils as du

async def create_center_graph_data(db_path, table, gui_q, case_number):
    graph_param = ['perfusion_time','art_flow','art_pressure','art_ph', 
        'ven_ph','art_pco2','art_po2','lactate','base','hb','hct','k','glucose'
        # 'fio2',
        # 'gas_flow',
        ]
    graph_data = du.get_val(db_path, table, graph_param, 1440, case_number)
    graph_item = oq.create_q_item('graph', 'main_panel', graph_data)
    print(f'create_center_graph_data -> graph data : {graph_item}')
    await oq.feed_queue(gui_q, graph_item)


# if __name__ == "__main__":
#     import os

#     table = 'test'
#     db_path = r'C:\Users\whwei\OneDrive\coding\data_vault.db'
#     create_center_graph_data(db_path, table, 2)
