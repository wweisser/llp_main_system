import db_main as dm
import db_utils as du
import cdi_connect as cc
import state_utils as su
import memory 
import onque as oq
import db_to_graph as dbtg
import asyncio
from datetime import datetime


async def parse_ser_input(msg: dict, sys_state, cache, key, gui_q):
    #is called form deque loop if there is a serial input. Parses the input put it to state and to gui.
    # print('message id : ', msg['id'])
    if msg['id'] == 'cdi':
        cdi_arr = cc.build_cdi_arr(msg['data'])
        sys_state = su.cdi_to_state(sys_state, cdi_arr)
        memory.put_state_to_cache(cache, key, sys_state)
        # que_item = oq.create_q_item('system', 'state', sys_state)
        # await oq.feed_queue(gui_q, que_item)
    return sys_state

async def parse_archive_request(msg: dict, sys_state: dict, ux_q, cache, key, parth, table):
    # print('message id : ', msg['id'])
    if msg['id'] == 'start_record':
        sys_state['system']['autosave'] = True
        sys_state['system']['start_time'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f'\nparse_archive_request -> Start time : {sys_state['system']['start_time']}\n')
        record_task = asyncio.create_task(dm.start_case_record(sys_state, ux_q, cache, key))
        if record_task:
            print('parse_archive_request -> recording has started')
            return record_task
    elif msg['id'] == 'stop_record':
        sys_state['system']['autosave'] = False
        memory.put_state_to_cache(cache, key, sys_state)
        print('parse_archive_request -> recording has stoped')
    elif msg['id'] == 'entry':
        print('parse_archive_request -> entry request was executed')
        await dm.db_entry(parth, table, msg['data'])

    # elif msg['id'] == 'data_request':
    #     val = msg['id']['val']
    #     range = msg['id']['range']
        # case_number = msg['id']['case_number']
        # dm.db_to_gui(gui_q, parth, val, range, case_number)
    elif msg['id'] == 'entry_request':
        pass
    elif msg['id'] == 'change_entry':
        pass
    return sys_state

async def parse_case_number_request(msg: dict, sys_state: dict, gui_q, parth: str, table: str):
    print('parse_case_number_request -> case_number input parser called')
    if msg['id'] == 'cn_asgn':
        sys_state['system']['case_number'] = msg['data']
    elif msg['id'] == 'list_request':
        print('\nparse_case_number_request -> Case umber list request received\n')
        val_arr = du.get_val(parth, table, 'case_number', -1, -1)
        if val_arr:
            que_item = oq.create_q_item('case_number', 'cn_list', val_arr)
            await oq.feed_queue(gui_q, que_item)
            print('parse_case_number_request -> list que item was created und fed to gui que : \n', que_item, '\n')
    elif msg['id'] == 'start_perfusion':
            sys_state['system']['autosave'] = True
            print(f'parse_case_number_request -> Autosave interval is set to {msg['data']} in sys_state to \n')
    else:
        pass
    return sys_state

async def parse_note_entry_request(msg: dict, sys_state: dict, gui_q):
    print('entry request')
    if msg['id'] == 'note':
        sys_state['notes'] = sys_state['notes'] + '\n' + msg['data']
        que_item = oq.create_q_item('system', 'state', sys_state)
        await oq.feed_queue(gui_q, que_item)
    return sys_state
    
async def parse_msg(msg: dict, sys_state, cache, key, gui_q, ux_q, parth: str, table: str):
    # print(f'Input parser called : {msg}')
    if msg['msg_type'] == 'ser_input':
        print('parse_msg -> serial input received')
        sys_state = await parse_ser_input(msg, sys_state, cache, key, gui_q)

    elif msg['msg_type'] == 'case_number':
        print('parse_msg -> case number request received')
        sys_state = await parse_case_number_request(msg, sys_state, gui_q, parth, table)

    elif msg['msg_type'] == 'archive':
        print('parse_msg -> archive request received')
        sys_state = await parse_archive_request(msg, sys_state, ux_q, cache, key, parth, table)
    
    elif msg['msg_type'] == 'entry_request':
        print('parse_msg -> entry request received')
        sys_state = await parse_note_entry_request(msg, sys_state, gui_q)

    else:
        print("parse_msg -> ux_q item is not valid")
        return None
    memory.put_state_to_cache(cache, key, sys_state)
    return sys_state

# start loop that fetches itmes from the input que
async def dequeue_loop(gui_q, ux_q, cache, key, path, table, system_tasks):
    sys_state = memory.get_state_from_cache(cache, key)
    print("DEQUELOOP HAS STARTED")
    while True:
        try:
            msg = await asyncio.wait_for(ux_q.get(), timeout=1.0)
            print('dequeue_loop -> msg: ', msg)
            if msg != '400'and isinstance(msg, dict):
                parse_object = await parse_msg(msg, sys_state, cache, key, gui_q, ux_q, path, table)
                if isinstance(parse_object, dict):
                    memory.put_state_to_cache(cache, key, parse_object)
                elif isinstance(parse_object, asyncio.Task):
                    system_tasks.append(parse_object)
        except Exception as e:
            print(e)


async def gui_updater(cache, key, gui_q, path:str, table:str):
    print('GUI UPDATER STARTED')
    current_time_old = datetime.now()
    while True:
        try:
            sys_state = memory.get_state_from_cache(cache, key)
            current_time = datetime.now()
            sys_state['system']['clock_time'] = current_time.strftime("%H:%M:%S")
            st = sys_state['system']['start_time']
            pt = sys_state['system']['perfusion_time']
            if sys_state['system']['autosave'] and st != 0:
                start_time_dt = datetime.strptime(st, "%d.%m.%Y %H:%M:%S")
                if pt != 0:
                    pt_old = datetime.strptime(pt, "%H:%M:%S")
                    pt = pt_old + (current_time - current_time_old)
                else:
                    pt = current_time - start_time_dt
                current_time_old = current_time
                h, remain = divmod(int(pt.total_seconds()), 3600)
                min, sec = divmod(remain, 60)
                sys_state['system']['perfusion_time'] = f"{h:02}:{min:02}:{sec:02}"
            memory.put_state_to_cache(cache, key, sys_state)
            gui_item = oq.create_q_item('system', 'state', sys_state)
            await oq.feed_queue(gui_q, gui_item)

            # if sys_state['system']['case_number'] != 0:
            #     dbtg.val_to_graph(path, table, 'art_ph', sys_state['system']['case_number'])


        except Exception as e:
            print('gui_updater -> ', e)
        await asyncio.sleep(1.0)