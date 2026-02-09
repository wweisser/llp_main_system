import threading as ts
import update_state as us
import onque as oq
import CDI_500_readout.ser_utils as con
import CDI_500_readout.db_utils as rs
from quart import websocket, Quart
import asyncio

def start_save_thread(serial_q,  mem, user_id, key_name):
    save_trd = ts.Thread(target=rs.save_trd, args=(serial_q, mem, user_id, key_name))
    save_trd.start()

def build_read_thread(serial_q, ser_arr):
    if serial_q and ser_arr:
        read_trd = ts.Thread(target=oq.ser_input_to_q, args=(serial_q, ser_arr))
        return read_trd

def build_dequeue_thread(serial_q, ux_q, mem, user_id, key_name):
    dequeue_trd = ts.Thread(target=us.dequeue_loop, args=(serial_q, ux_q, mem, user_id, key_name))
    return dequeue_trd

def join_thread(thread):
    if thread:
        thread.join()
    return thread

async def start_system(database_path, gui_q, ux_q, serial_q, cache, key):
    ser_arr = con.create_all_sp()
    ser_arr = con.open_all_sp(ser_arr)
    # print("serial que: ", serial_q, "memory: ", mem, "user id: ", user_id, "key_name: ", key_name)
    if not serial_q:
        print("serial_q ist 'falsy'")
    if not cache:
        print("cache ist 'falsy'")
    if not key:
        print("key ist 'falsy'")
    if serial_q and cache and key:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(us.dequeue_loop(gui_q, ux_q, cache, key))
            tg.create_task(oq.ser_input_to_q(ux_q, ser_arr))
            print("starting system")
        # read_trd = build_read_thread(serial_q, ser_arr)
        # deque_trd = build_dequeue_thread(serial_q, ux_q, mem, user_id, key_name)
        # if put_io_que and fetch_io_que:
            # read_trd.start()
            # deque_trd.start()


