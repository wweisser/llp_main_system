import onque as oq
import db_utils as du

async def create_center_graph_data(db_path, table, gui_q, case_number):
    graph_param = ['clock_time','ven_pco2','ven_po2','art_ph', 
        'ven_ph','art_pco2','art_po2','hco3','base','cso2','hct','k','glucose', 'lactate'
        # 'fio2',
        # 'gas_flow',
        ]
    graph_data = du.get_val(db_path, table, graph_param, 1440, case_number)
    graph_item = oq.create_q_item('metabolic_graph_store', 'metabolic_graph_store', graph_data)
    print(f'create_center_graph_data -> graph graph item was created')
    await oq.feed_queue(gui_q, graph_item)

# async def create_note_data(db_path, table, case_number, current_str):
#     note_data = du.get_val(db_path, table, ['notes',] , 1440, case_number)
#     note_str = ''
#     for note in note_data:
#         note_str.append(f'{note[0]}: {note[1]}\n')
#     note_str.append(current_str)
#     return

# if __name__ == "__main__":
#     import os

#     table = 'test'
#     db_path = r'C:\Users\whwei\OneDrive\coding\data_vault.db'
#     create_center_graph_data(db_path, table, 2)
