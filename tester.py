#import serial
import random
import system_update as su
import state
import memory
import onque as oq
import ser_connection as sc
import gui
import asyncio
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from fastapi.middleware.wsgi import WSGIMiddleware 

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
            q_item = oq.create_q_item('serial', 'cdi', test_barr)
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
    tx_q = asyncio.Queue()
    gui_q = asyncio.Queue()
    sys_state = state.create_state(database_path)
    cache = memory.create_cache(cache_path, key, sys_state)
    return gui_q, ux_q, tx_q, cache

# trys to receive a mesage and puts it on an input que 
async def ws_recv(websocket, ux_q):
    print(f'ws_recv -> recv loop was started')
    while True:
        try:
            msg_raw = await websocket.receive_json() 
            # print(f'ws_recv -> msg raw {msg_raw}') 
            # msg = state.get_json(msg_raw)
            # print(f'ws_recv -> msg {msg}') 

            await ux_q.put(msg_raw)
        except WebSocketDisconnect as e:
            raise 
        except Exception as e:
            print("ws_recv -> could not receive")
            print(e)

# fetches item from gui que and trys to send via websocket
async def ws_send(websocket, gui_q):
    print(f'ws_send -> send loop was started')
    while True:
        try:
            msg = await gui_q.get()
            if isinstance(msg, dict):
                msg_to_send = json.dumps(msg)
                await websocket.send_text(msg_to_send)
            else:
                print('ws_send -> item to send was not dict')
        except WebSocketDisconnect as e:
            raise
        except Exception as e:
            print('ws_send -> could not send')
            print(e)

async def start_ws(app, gui_q, ux_q):
#starts websocket and calls in every iteration of the while loop recv and send function
    print('STARTING WEBSOCKET')
    @app.websocket("/ws") # hier wird das websocket an die fastAPI app gebunden
    async def endpoint(ws: WebSocket):
        await ws.accept() # hier wird der serverhandshake durchgeführt
        try:
            print('\nstart_ws -> WEBSOCKET ONLINE\n')
            async with asyncio.TaskGroup() as tg:
                    tg.create_task(ws_recv(ws, ux_q))
                    tg.create_task(ws_send(ws, gui_q))
        except* WebSocketDisconnect:
            print("Verbindung getrennt ")
        except* Exception as e:
            print(f"Fehler: {e}")


async def create_system_tasks(app, sp):
    system_tasks = []
    try:
        system_tasks.append(asyncio.create_task(start_ws(app, sp['gui_q'], sp['ux_q'])))
        system_tasks.append(asyncio.create_task(su.dequeue_loop(sp, system_tasks)))
        # system_tasks.append(asyncio.create_task(sc.connection_handler(sp['ux_q'], sp['tx_q'])))
        system_tasks.append(asyncio.create_task(su.gui_updater(sp['cache'], sp['key'], sp['gui_q'])))
################TEST TEST TEST#########################################
        system_tasks.append(asyncio.create_task(start_cdi_test_thread(sp['ux_q'])))
################TEST TEST TEST#########################################
        return system_tasks
    except Exception as e:
        print(f'create_system_tasks -> error on system task setup\n', e)
        return None
    
def create_sys_param(gui_q, ux_q, tx_q, cache, key, com_port_hub, db_path, table):
    sp = {
        "gui_q": gui_q, 
        "ux_q": ux_q,
        "tx_q": tx_q, 
        "cache": cache, 
        "key": key,
        "com_port_hub": com_port_hub,
        "db_path": db_path,
        "table": table,
        "system_runtime": 0,
    }
    return sp

async def main():
    key = "key_name"
    table = 'test'
    db_path = r'C:\Users\whwei\OneDrive\coding\data_vault.db'
    cache_path = r'C:\Temp\diskcache_test'
    gui_q, ux_q, tx_q, cache = build_state(cache_path, db_path, key)
    com_port_hub = None
    sp = create_sys_param(gui_q, ux_q, tx_q, cache, key, com_port_hub, db_path, table)

    try:
        fast_api_app = FastAPI() # hier wird die fastAPI app erzeugt
        fast_api_app.mount("/d1/", WSGIMiddleware(gui.app.server)) 
        #Hier wird ads snchron laufende dash mit dem asynchronen fastAPI via WSGI verbunden

        @fast_api_app.get("/health")
        def health():
            return {"status": "ok"}

        @fast_api_app.get("/")
        def index():
            return RedirectResponse(url="/d1/")
        
        system_tasks = await create_system_tasks(fast_api_app, sp)
        config = uvicorn.Config(fast_api_app, host="0.0.0.0", port=8050, log_config=None)
        # hier wird die serverkonfiguration für den guvicorn server erstellt
        server = uvicorn.Server(config)
        # Hier wird der die app an uvicorn(name für das serverframwork) übergeben
        await asyncio.gather(server.serve(), *system_tasks)
    except Exception as e:
        for task in system_tasks:
            task.cancel()           # Beim App-Shutdown: Task abbrechen
            try:
                await task          # Warten bis der Task wirklich gestoppt ist
            except asyncio.CancelledError:
                print(f'main -> {task} was stoped')
        print("main -> system was closed")
        print(e)
    
    # system_tasks = await create_system_tasks(fast_api_app, key, cache, db_path, table, gui_q, ux_q)


if __name__ == "__main__":
    # main()
    asyncio.run(main())


#URL : http://127.0.0.1:8050/d1/