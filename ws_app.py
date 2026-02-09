from quart import websocket, Quart
import asyncio
from hypercorn.asyncio import serve, Config
import state

# trys to receive a mesage and puts it on an input que 
async def recv(ux_q):
    try:
        msg_to_recv = await asyncio.wait_for(websocket.receive(), timeout=0.01)
        msg = state.get_json(msg_to_recv)
        print('unjsoned msg back from frontend type : ', type(msg), msg )
        await ux_q.put(msg)
    except Exception as e:
        print("could not receive")
        print(e)

# fetches item from gui que and trys to send via websocket
async def send(gui_q):
    msg_to_send = await gui_q.get()
    msg = state.pack_json(msg_to_send)
    try:
        await websocket.send(msg)
        print('MSG send : ', msg)
    except Exception as e:
        print("could not send")
        print(e)

#starts websocket and calls in every iteration of the while loop recv and send function
def start_ws(app, gui_q, ux_q):
    @app.websocket("/ws")
    async def random_data():
        await websocket.accept()
        print('websocket START')
        while True:
            await send(gui_q)
            # await recv(ux_q)

# # creates and start the quart app
# async def start_bknd(gui_q, ipt_q):
#     app = Quart(__name__)
#     config = Config()
#     config.bind = ["127.0.0.1:5000"]

#     server = asyncio.create_task(serve(app, config))
#     start_ws(app, gui_q, ipt_q)
#     put_task = asyncio.create_task(fill_gui_q(gui_q))
#     fetch_task = asyncio.create_task(fetch_ipt_q(ipt_q))
#     # await server
#     await asyncio.gather(server, put_task, fetch_task)

# def create_bknd_task():
#     asyncio.run(start_bknd())