from quart import websocket, Quart
import asyncio
from hypercorn.asyncio import serve, Config
import random
import json
from datetime import datetime as dt
# from hypercorn.config import Config


async def fill_gui_q(gui_q):
    while True:
        try:
            item = str(random.randrange(1,100))
            await gui_q.put(item)
            print(f"{item} is put to gui que")
            await asyncio.sleep(3)
        except:
            print("could not send")

async def fetch_ipt_q(ipt_q):
    while True:
        try:
            item = await ipt_q.get()
            print('item received from ipt_q: ', item['number'])
        except Exception as e:
            print('could not unload ipt_q')
            print(e)

async def recv(ipt_q):
    try:
        msg = await asyncio.wait_for(websocket.receive(), timeout=0.1)
        item = json.loads(msg)
        await ipt_q.put(item)
    except Exception as e:
        print("could not receive")
        print(e)

async def send(gui_q):
    item = await gui_q.get()
    jsn_content= {
        'type': 'digit',
        'number': item
    }
    msg = json.dumps(jsn_content)
    try:
        await websocket.send(msg)
    except:
        print("could not send")

def start_ws(app, gui_q, ipt_q):
    print('\nWEBSOCKET WAS CREATED\n')
    @app.websocket("/ws")
    async def random_data():
        await websocket.accept()
        print(f'\nWEBSOCKET WAS STARTED\n')
        while True:
            await recv(ipt_q)
            await send(gui_q)


async def start_bknd():
    gui_q = asyncio.Queue()
    ipt_q = asyncio.Queue()
    app = Quart(__name__)
    config = Config()
    config.bind = ["127.0.0.1:5000"]

    server = asyncio.create_task(serve(app, config))
    start_ws(app, gui_q, ipt_q)
    put_task = asyncio.create_task(fill_gui_q(gui_q))
    fetch_task = asyncio.create_task(fetch_ipt_q(ipt_q))
    # await server
    await asyncio.gather(server, put_task, fetch_task)

def create_bknd_task():
    asyncio.run(start_bknd())

if __name__ == "__main__":
    create_bknd_task()