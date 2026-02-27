import serial
import random
import update_state as us
import state
import memory
import onque as oq
import ser_connection as sc
import gui
import asyncio
import json
import uvicorn
from fastapi import FastAPI, WebSocket
from dash import Dash
# from gui import app as dashboard1
from fastapi.middleware.wsgi import WSGIMiddleware

# from quart import websocket, Quart
from hypercorn.asyncio import serve, Config

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
    print('start_cdi_test_thread -> CDI 500 test thread was started')
    while True:
        test_barr = ""
        test_barr = create_test_bytearray()
        if test_barr != "":
            q_item = sc.input_to_q_item(test_barr)
        await oq.feed_queue(q, q_item)
        await asyncio.sleep(6)

async def test_intput_process(gui_q, ux_q):
    print('input process test')
    ux_item = create_postbox_item('case_number', 'list_request', '')
    print(f'\nITEM TO UX QUE, TYPE : {type(ux_item)}, CONTENT : \n', ux_item)
    ux_input = json.loads(ux_item)
    await oq.feed_queue(ux_q, ux_input)
    gui_item = await gui_q.get()
    print('\nITEM FETCHED FROM GUI QUE : \n', gui_item)

################TEST TEST TEST#########################################

def build_state(cache_path: str, database_path: str, key:str):
    ux_q = asyncio.Queue()
    gui_q = asyncio.Queue()
    sys_state = state.create_state(database_path)
    cache = memory.create_cache(cache_path, key, sys_state)
    return gui_q, ux_q, cache

# trys to receive a mesage and puts it on an input que 
async def ws_recv(websocket, ux_q):
    while True:
        try:
            print('ws_recv -> waiting for incomig message')
            msg_raw= await websocket.receive()
            if msg_raw and isinstance(msg_raw, dict):
                if msg_raw['type'] == 'websocket.disconnect':
                    print('ws_recv -> websocked disconnected')
                    break    
            print('ws_recv -> ', msg_raw, 'type : ', type(msg_raw))
            msg = state.get_json(msg_raw['text'])
            print('ws_recv -> unjsoned msg : ', msg, type(msg) )
            await ux_q.put(msg)
        except Exception as e:
            print("ws -> could not receive")
            print(e)

# fetches item from gui que and trys to send via websocket
async def ws_send(websocket, gui_q):
    while True:
        try:
            msg = await gui_q.get()
            if isinstance(msg, dict):
                msg_to_send = json.dumps(msg)
                print('ws_send -> message to send', type(msg_to_send))
                await websocket.send_text(msg_to_send)
                print('ws_send -> item was send')
            else:
                print('ws_send -> item to send was not dict')
        except Exception as e:
            print('ws_send -> could not send')
            print(e)

def start_ws(app, gui_q, ux_q):
#starts websocket and calls in every iteration of the while loop recv and send function
    print('STARTING WEBSOCKET')
    @app.websocket("/ws")
    async def ws(websocket: WebSocket):
        await websocket.accept()
        print('\nstart_ws -> WEBSOCKET ONLINE\n')
        recv_task = asyncio.create_task(ws_recv(websocket, ux_q))
        send_task = asyncio.create_task(ws_send(websocket, gui_q))
        await asyncio.gather(recv_task, send_task)

async def create_system_tasks(app, key, cache, db_path, table, gui_q, ux_q):
    system_tasks = []
    if app and gui_q and ux_q:
        system_tasks.append(asyncio.create_task(us.dequeue_loop(gui_q, ux_q, cache, key, db_path, table, system_tasks)))
        # system_tasks.append(asyncio.create_task(sc.connection_handler(ux_q)))
        system_tasks.append(asyncio.create_task(us.gui_updater(cache, key, gui_q, db_path, table)))
################TEST TEST TEST#########################################
        system_tasks.append(asyncio.create_task(start_cdi_test_thread(ux_q)))
################TEST TEST TEST#########################################
        # await asyncio.gather(*system_tasks)
        return system_tasks
    else:
        return None



async def main():
    key = "key_name"
    table = 'test'
    db_path = r'data_vault.db'
    cache_path = r'C:\Temp\diskcache_test'
    gui_q, ux_q, cache = build_state(cache_path, db_path, key)

    try:
        fast_api_app = FastAPI()
        fast_api_app.mount("/dashboard1", WSGIMiddleware(gui.app.server))
        start_ws(fast_api_app, gui_q, ux_q)
        @fast_api_app.get("/")
        def index():
            return "Hello"
    except Exception as e:
        print("main -> server client collapsed")
        print(e)
    system_tasks = await create_system_tasks(fast_api_app, key, cache, db_path, table, gui_q, ux_q)
    config = uvicorn.Config(fast_api_app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()
    await asyncio.gather(*system_tasks)


if __name__ == "__main__":
    # main()
    asyncio.run(main())


# async def start_backend(quart_app, cache_path, db_path, key, table):
#     config = Config()
#     config.bind = ["127.0.0.1:5000"]
#     gui_q, ux_q, cache = build_state(cache_path, db_path, key)
#     # json_data = memory.fetch_from_cache(cache, key)
#     system_tasks = []    
#     if quart_app and gui_q and ux_q:
#         # async with asyncio.TaskGroup() as tg:
#         #     tg.create_task(us.dequeue_loop(gui_q, ux_q, cache, key, db_parth, table))
#         #     # tg.create_task(sc.connection_handler(ux_q))
#         #     tg.create_task(serve(qart_app, config))
#         #     tg.create_task(us.gui_updater(cache, key, gui_q))
#         system_tasks.append(asyncio.create_task(us.dequeue_loop(gui_q, ux_q, cache, key, db_path, table, system_tasks)))
#         # system_tasks.append(asyncio.create_task(sc.connection_handler(ux_q)))
#         system_tasks.append(asyncio.create_task(serve(quart_app, config)))
#         system_tasks.append(asyncio.create_task(us.gui_updater(cache, key, gui_q, db_path, table)))

# ################TEST TEST TEST#########################################
#         system_tasks.append(asyncio.create_task(start_cdi_test_thread(ux_q)))
#             # tg.create_task(start_cdi_test_thread(ux_q))
#             # tg.create_task(test_intput_process(gui_q, ux_q))
# ################TEST TEST TEST#########################################
#         await asyncio.gather(*system_tasks)

# async def test_env():
#     key = "key_name"
#     table = 'test'
#     db_parth = r'data_vault.db'
#     cache_path = r'C:\Temp\diskcache_test'

#     qart_app = Quart(__name__)

#     config = Config()
#     config.bind = ["127.0.0.1:5000"]

#     gui_q, ux_q, cache = build_state(cache_path, db_parth, key)
#     # json_data = memory.fetch_from_cache(cache, key)
#     system_tasks = []
#     start_ws(qart_app, gui_q, ux_q)
#     if qart_app and gui_q and ux_q:
#         # async with asyncio.TaskGroup() as tg:
#         #     tg.create_task(us.dequeue_loop(gui_q, ux_q, cache, key, db_parth, table))
#         #     # tg.create_task(sc.connection_handler(ux_q))
#         #     tg.create_task(serve(qart_app, config))
#         #     tg.create_task(us.gui_updater(cache, key, gui_q))
#         system_tasks.append(asyncio.create_task(us.dequeue_loop(gui_q, ux_q, cache, key, db_parth, table, system_tasks)))
#         # system_tasks.append(asyncio.create_task(sc.connection_handler(ux_q)))
#         # system_tasks.append(asyncio.create_task(serve(qart_app, config)))
#         system_tasks.append(asyncio.create_task(us.gui_updater(cache, key, gui_q, db_parth, table)))

# ################TEST TEST TEST#########################################
#         system_tasks.append(asyncio.create_task(start_cdi_test_thread(ux_q)))
#             # tg.create_task(start_cdi_test_thread(ux_q))
#             # tg.create_task(test_intput_process(gui_q, ux_q))
# ################TEST TEST TEST#########################################
#         await asyncio.gather(*system_tasks)
    # dash_app = gui.run_app(qart_app)
    # # qart_app.wsgi_app = dash_app.server
    # @qart_app.route('/api')
    # async def get_data():    
    #     return {'status': 'success'}
# if __name__ == '__main__':

# def main():
#     key = "key_name"
#     table = 'test'
#     db_parth = r'data_vault.db'
#     cache_path = r'C:\Temp\diskcache_test'

#     gui_q, ux_q, cache = build_state(cache_path, db_parth, key)
#     try:
#         fast_api_app = FastAPI()
#         fast_api_app.mount("/dashboard1", WSGIMiddleware(gui.app.server))
#         start_ws(fast_api_app, gui_q, ux_q)
#         @fast_api_app.get("/")
#         def index():
#             return "Hello"
#     except Exception as e:
#         print("main -> server client collapsed")
#         print(e)

#     uvicorn.run(fast_api_app, host="127.0.0.1")

# if __name__ == "__main__":
#     main()
# asyncio.run(main())