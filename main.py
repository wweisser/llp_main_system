# import CDI_500_readout.db_main as dm
# import CDI_500_readout.ser_utils as con
# import update_state as us
# import threads as ts
# import queue
# import state
# import memory
# import gui

# import tester

# def build_state(database_path, user_id, key_name):
#     q = queue.Queue()
#     sys_state = state.create_state()
#     mem = memory.create_memory(database_path, sys_state, user_id, key_name)
#     return q, sys_state, mem

# # insert comports
# def build_gui(q, mem, user_id, key_name):
#     comport_arr = ['',]
#     gui.run_app(mem, user_id, key_name)
#     con.start_read_thread(q, comport_arr, memory, user_id, key_name)
#     us.start_dequeue_thread(q, mem, user_id, key_name)
#     # update of gui via intervall callback

# if __name__ == '__main__':
#     tester.send_test_str("COM1")
#     com_arr = ['COM2',]
#     user_id = "user_id"
#     key_name = "key_name"
#     q, ser_arr, sys_state, mem = build_state(None, "user_id", "key_name", com_arr)
#     trd, trd_deque = ts.create_threads(q, ser_arr, mem, user_id, key_name)
#     ts.start_thread(trd)
#     ts.start_thread(trd_deque)
#     gui.run_app(mem, user_id, key_name)
#     # ts.join_thread(trd)
#     # ts.join_thread(trd_deque)









# def run_cdi(port, cursor, connector, case_number: str):
#     while(True):
#         serial_read = sp.read_data(port)
#         cdi_val = cc.cdi(serial_read)
#         print(cdi_val)
#         dm.update_database(cursor, connector, cdi_val, case_number)
#         time.sleep(3)

# def run_system():
#     init.create_cn_table()
#     start_time = datetime.datetime.now()
#     print(start_time)
#     case_number = start_time.strftime('%Y%m%d%H%M%S')
#     str_case_number = f"{case_number}"
#     conn = sqlite3.connect('data.db')
#     c = conn.cursor()
#     # database.create_table(c, conn, str_case_number)
#     app.app.run(debug=True)
#     # sp1 = serial_ports.open_serial('COM1', 'CDI500')
#     # t1 = threading.Thread(target=run_cdi, args=(sp1, c, conn))
#     # t1.start()