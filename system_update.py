import memory 
import onque as oq
import system_parse
import asyncio
import db_que as dbq
from datetime import datetime



# start loop that fetches itmes from the input que
async def dequeue_loop(db_que: dbq.Db_Que, ux_q, com_q: asyncio.Queue, cc: dict):
    """Starts the main loop that listens to the ux_q. If the dequed object is a dict, parse_msg is called.
    If the return of parsed_msg is an asyncio.Task, that task is added to the system_tasks"""
    print("DEQUELOOP STARTED")
    while True:
        # try:
            msg = await ux_q.get()
            sys_state = memory.get_state_from_cache(db_que.db_obj.cache, db_que.db_obj.key)

            if isinstance(msg, dict):
                sys_state = await system_parse.parse_msg(db_que, com_q, msg, sys_state=sys_state, cc=cc)
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
