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
    # table = 'test'
    # db_path = r'data_vault.db'
    # create_graph_figure(db_path, table, 'art_ph', 1)
    datetime.now().strftime("%d-%m-%Y %H:%M")




