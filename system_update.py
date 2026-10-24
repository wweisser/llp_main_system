import memory 
import onque as oq
import system_parse
import asyncio
import db_que as dbq
from datetime import datetime

def generate_one_beat(status: str):
    b_heartbeat = {
        'last_heartbeat': int(datetime.now().timestamp()),
        'status': status,
        'error_state': None,
    }
    return b_heartbeat

def genertate_graph_output():
    pass

# start loop that fetches itmes from the input que
async def dequeue_loop(db_que: dbq.Db_Que, ux_q, system_tasks: list, cc: dict):
    """Starts the main loop that listens to the ux_q. If the dequed object is a dict, parse_msg is called.
    If the return of parsed_msg is an asyncio.Task, that task is added to the system_tasks"""
    print("DEQUELOOP STARTED")
    while True:
        # try:
            msg = await ux_q.get()
            # print(f'dequeue_loop -> msg: {msg}')
            sys_state = memory.get_state_from_cache(db_que.db_obj.cache, db_que.db_obj.key)
            if isinstance(msg, dict):
                sys_state = await system_parse.parse_msg(db_que, msg, sys_state=sys_state, cc=cc)
                memory.put_state_to_cache(db_que.db_obj.cache, db_que.db_obj.key, sys_state)
        # except Exception as e:
        #     print('error during deque loop\n', e)

def calc_perfusion_time(start_time):
    if start_time:
        current_time = datetime.now()
        pt = current_time - start_time
        return pt
    else:
        return 0

async def b_heartbeat(cc, intervall: float):
    print('BACKEND HEARTBEAT STARTED')
    while True:
        b_heartbeat_item = generate_one_beat("backend_active")
        await oq.broadcast_item('heartbeat', 'status', b_heartbeat_item, cc)
        await asyncio.sleep(intervall)

# async def system_updater(cache, key, archive_intervall: int, update_intervall: float):
#     """System updater loop that updates the system state every set interval.
#     Perfusion time and clock time and archive funktion"""
#     counter = 0
#     while True:
#         ct = datetime.now()
#         sys_state = memory.get_state_from_cache(cache, key)
#         if sys_state and ct:
#             sys_state['system']['clock_time'] = ct

#         if sys_state['system']['autosave'] and sys_state['system']['start_time'] != 0:
#             sys_state = calc_perfusion_time(sys_state, sys_state['system']['start_time'])
#             memory.put_state_to_cache(cache, key, sys_state)

#         if counter > archive_intervall:
#             counter = 0
#         counter += 1
#         await asyncio.sleep(update_intervall)
