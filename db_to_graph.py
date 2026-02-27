import sqlite3
import plotly.graph_objects as go


# def val_to_graph(parth: str, table: str, val: str, case_number: int) -> go.Figure:
#     with sqlite3.connect(parth) as conn:
#         c = conn.cursor()
#         c.execute(f"PRAGMA table_info({table})")
#         columns = {row[1] for row in c.fetchall()}

#         if val not in columns:
#             raise ValueError(f"Invalid column name: '{val}'")

#         c.execute(
#             f"SELECT perfusion_time, {val} FROM {table} WHERE case_number = ? ORDER BY id DESC LIMIT 1000",
#             (case_number,)
#         )
#         rows = c.fetchall()
#         print('val_to_graph -> ', rows)
#     rows = list(reversed(rows))
#     x = [row[0] for row in rows]
#     y = [row[1] for row in rows]

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name=val))
#     fig.update_layout(
#         xaxis_title='Perfusion Time',
#         yaxis_title=val
#     )
#     return fig

# if __name__ == '__main__':
#     fig = val_to_graph('data_vault.db', 'test', 'art_ph', 3)