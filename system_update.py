import memory 
import onque as oq
import system_parse
import asyncio
import db_que as dbq
from datetime import datetime


def calc_perfusion_time(start_time):
    if start_time:
        current_time = datetime.now()
        pt = current_time - start_time
        return pt
    else:
        return 0


# start loop that fetches itmes from the input que
async def dequeue_loop(db_que: dbq.Db_Que, ux_q: asyncio.Queue, com_q: asyncio.Queue, cc: dict):
    """Starts the main loop that listens to the ux_q. If the dequed object is a dict, parse_msg is called.
    If the return of parsed_msg is an asyncio.Task, that task is added to the system_tasks"""
    print("DEQUELOOP STARTED")
    while True:
        msg = None
        now = int(datetime.now().timestamp())
        sys_state = memory.get_state_from_cache(db_que.db_obj.cache, db_que.db_obj.key)

        if (now - sys_state['last_graphs_update']) > 10:
            await db_que.put_db_item('ext', anex='graphs', case_id=sys_state['case_id'])
            sys_state['last_graphs_update'] = now

        try:
            msg = await asyncio.wait_for(ux_q.get(), timeout=0.5)
        except TimeoutError:
                pass
        except Exception as e:
                print(f'Error during system update: {e}')

        if msg != None and isinstance(msg, dict):
            # try:
            sys_state = await system_parse.parse_msg(db_que, com_q, ux_q, msg, sys_state, cc)
            # except Exception as e:
            #     print(f'Error during system parse: {e}')

        memory.put_state_to_cache(db_que.db_obj.cache, db_que.db_obj.key, sys_state)



