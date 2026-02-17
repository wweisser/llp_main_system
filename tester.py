import serial
import random
import update_state as us
import state
import memory
import onque as oq
import ser_connection as sc
import asyncio
import json

from quart import websocket, Quart
from hypercorn.asyncio import serve, Config

################TEST TEST TEST#########################################

def build_state(cache_path: str, database_path: str, key:str):
    ux_q = asyncio.Queue()
    gui_q = asyncio.Queue()
    sys_state = state.create_state(database_path)
    cache = memory.create_cache(cache_path, key, sys_state)
    # sys_state = await memory.get_user_value(cache, key)
    # print('sys_state : ', sys_state)
    return gui_q, ux_q, cache

# trys to receive a mesage and puts it on an input que 
async def recv(ux_q):
    while True:
        try:
            print('ws -> waiting for incomig message')
            msg_raw= await websocket.receive()
            print(msg_raw)
            msg = state.get_json(msg_raw)
            await ux_q.put(msg)
            print('ws -> unjsoned msg back from frontend type : ', type(msg), msg)
        except Exception as e:
            print("ws -> could not receive")
            print(e)

# fetches item from gui que and trys to send via websocket
async def send(gui_q):
    while True:
        try:
            msg = await gui_q.get()
            msg_to_send = json.dumps(msg)
            await websocket.send(msg_to_send)
            # print('ws -> item was send')
        except Exception as e:
            print("ws -> could not send")
            print(e)

def start_ws(app, gui_q, ux_q):
#starts websocket and calls in every iteration of the while loop recv and send function
    print('STARTING WEBSOCKET')
    @app.websocket("/ws")
    async def ws():
        await websocket.accept()
        print('\nWEBSOCKET ONLINE\n')
        # while True:
            # CONTINUE HERE SEND UND RECV HAVE TO ALIGN #
        print('ws loop active')
        recv_task = asyncio.create_task(recv(ux_q))
        send_task = asyncio.create_task(send(gui_q))
        await asyncio.gather(recv_task, send_task)

################TEST TEST TEST#########################################

def create_postbox_item(msg_type: str, id: str, data):
    msg_item = {
        'msg_type': 'ux',
        'id': '',
        'data': ''
    }
    if msg_type:
        msg_item['msg_type'] = msg_type
    if id:
        msg_item['id'] = id
    if data:
        msg_item['data'] = data
    msg_item = json.dumps(msg_item)
    return msg_item

def create_test_bytearray():
    art_ph = round(random.uniform(7.3, 7.5), 2)
    art_CO2 = random.randint(35, 45)
    art_O2 = random.randint(100, 150)
    ven_ph = round(random.uniform(7.2, 7.4), 2)
    ven_CO2 = random.randint(45, 55)
    ven_O2 = random.randint(50, 100)
    cSO2 = random.randint(95, 100)
    SO2 = random.randint(95, 100)
    hb = round(random.uniform(6.5, 8.5), 1)
    k = round(random.uniform(3.1, 6.9), 1)
    hct = random.randint(18, 24)
    base = random.randint(-10, 4)
    hco3 = random.randint(18, 24)

    # Time pH CO2 O2 Temp HCO3 BE cSO2 K+ VO2 Q BSA pH CO2 O2 Temp SO2 HCT HGB

                 #b' 09:41:33\t7.44\         t 042\            t 148\          t26.4\t 21 \t -1 \   t 95\          t 4.5 \       t ---\     t    \t    \t7.33\         t54  \          t 50 \          t25.5\      t 98 \        t 18 \       t 6.6\        r\n'
    test_string = f' 09:41:33\t{str(art_ph)}\t 0{str(art_CO2)}\t {str(art_O2)}\t26.4\t {str(hco3)} \t {str(base)} \t {str(cSO2)} \t {str(k)}\t ---\t    \t{str(ven_ph)}\t{str(ven_CO2)}  \t {str(ven_O2)} \t ---\t25.5\t {str(SO2)} \t {str(hct)} \t {str(hb)}\r\n'
    # cdi_string = b' 13:13:25\t6.58\t 035\t ---\t35.8\t 03 \t -- \t ---\t -.-\t ---\t -.-\t    \t6.67\t 027\t ---\t35.1\t ---\t ---\t -.-\r\n'

    test_bytearray = bytearray(test_string, "utf-8")
    return test_bytearray

async def start_cdi_test_thread(q):
    while True:
        test_barr = ""
        test_barr = create_test_bytearray()
        if test_barr != "":
            q_item = sc.input_to_q_item(test_barr)
        await oq.feed_queue(q, q_item)
        await asyncio.sleep(4)

async def test_intput_process(gui_q, ux_q):
    print('input process test')
    ux_item = create_postbox_item('case_number', 'list_request', '')
    print(f'\nITEM TO UX QUE, TYPE : {type(ux_item)}, CONTENT : \n', ux_item)
    ux_input = json.loads(ux_item)
    await oq.feed_queue(ux_q, ux_input)
    gui_item = await gui_q.get()
    print('\nITEM FETCHED FROM GUI QUE : \n', gui_item)

################TEST TEST TEST#########################################

async def test_env():
    key = "key_name"
    table = 'test'
    db_parth = r'data_vault.db'
    cache_path = r'C:\Temp\diskcache_test'

    qart_app = Quart(__name__)

    config = Config()
    config.bind = ["127.0.0.1:5000"]

    gui_q, ux_q, cache = build_state(cache_path, db_parth, key)
    # json_data = memory.fetch_from_cache(cache, key)

    start_ws(qart_app, gui_q, ux_q)
    if qart_app and gui_q and ux_q:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(us.dequeue_loop(gui_q, ux_q, cache, key, db_parth, table))
            # tg.create_task(sc.connection_handler(ux_q))
            tg.create_task(serve(qart_app, config))
################TEST TEST TEST#########################################
            tg.create_task(start_cdi_test_thread(ux_q))
            # tg.create_task(test_intput_process(gui_q, ux_q))
################TEST TEST TEST#########################################

# if __name__ == '__main__':

async def main():
    await test_env()


asyncio.run(main())