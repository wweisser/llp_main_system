import plotly.graph_objects as plgo
import db_utils as dbu
from datetime import datetime

def create_graph_figure(path: str, table: str, val: str, case_number):
    if isinstance(case_number, str) and case_number.isdigit():
        case_number = int(case_number)


    x_axis = dbu.get_val(path, table, "perfusion_time", 1000, case_number)
    y_axis = dbu.get_val(path, table, val, 1000, case_number)
    figure = plgo.Figure(data=plgo.Scatter(x_axis, y_axis))
    return figure


if __name__ == "__main__":
    note_data = {'notes': ['test string 1', 'test string 1', 'test string 2', 'test string 3', 'test string 4', 'test string 4']}
    note_str = result = '\n'.join(note_data['notes'])
    print(note_str)
    # for note in note_data:
    #     note_str = note_str.join(note_data[note])
    # print(f'parse_archive_request -> note : {note_data[note]}\n')





