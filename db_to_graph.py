import sqlite3
import plotly.express as px
import db_main as dm
import db_utils as du
import pandas as pd

def build_graph_object(db_path, table, param):
    val_arr = du.get_val(db_path, table, param, 1000, 1)

    df = pd.DataFrame({
        "time": val_arr[0],
        "param": val_arr[1]
    })

    fig = px.line(df, x="time", y="param")
    print(fig)


if __name__ == "__main__":
    table = 'test'
    db_path = r'C:\Users\whwei\OneDrive\coding\data_vault.db'
    build_graph_object(db_path, table, 'art_flow')