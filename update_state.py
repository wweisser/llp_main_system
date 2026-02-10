import db_main as dm
import db_utils as du
import cdi_connect as cc
import state_utils as su
import memory 
import onque as oq
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

async def parse_archive_request(msg: dict, sys_state: dict, cache, key, parth, table, gui_q):
    # print('message id : ', msg['id'])
    if msg['id'] == 'start_record':
        sys_state['system']['autosave'] = asyncio.create_task(dm.start_autosave(cache, key, parth, table))
        sys_state['system']['start_time'] = datetime.now()
    elif msg['id'] == 'stop_record':
        sys_state['autosave'] = False
        memory.put_state_to_cache(cache, key, sys_state)
    elif msg['id'] == 'entry':
        dm.db_entry(parth, table, sys_state)
    elif msg['id'] == 'data_request':
        val = msg['id']['val']
        range = msg['id']['range']
        # case_number = msg['id']['case_number']
        # dm.db_to_gui(gui_q, parth, val, range, case_number)
    elif msg['id'] == 'entry_request':
        pass
    elif msg['id'] == 'change_entry':
        pass
    return sys_state

async def parse_case_number_request(msg: dict, sys_state: dict, parth: str, table: str, gui_q):
    print('case_number input parser called')
    if msg['id'] == 'cn_asgn':
        sys_state['system']['case_number'] = msg['data']
        que_item = oq.create_q_item('system', 'state', sys_state)
        await oq.feed_queue(gui_q, que_item)
    elif msg['id'] == 'list_request':
        print('\nCase umber list request received\n')
        val_arr = du.get_val(parth, table, 'case_number', -1, -1)
        que_item = oq.create_q_item('case_number', 'cn_list', val_arr)
        await oq.feed_queue(gui_q, que_item)
        # print('list que item was created und fed to gui que : \n', que_item, '\n')
    elif msg['id'] == 'start_perfusion':
        if isinstance(msg['data'], int):
            sys_state['system']['autosave'] = msg['data']
            print(f'Autosave interval is set to {msg['data']} in sys_state to \n')
    else:
        pass
    return sys_state
    
async def parse_msg(msg: dict, sys_state, cache, key, gui_q, parth: str, table: str):
    print('Input parser called')
    if msg['msg_type'] == 'ser_input':
        sys_state = await parse_ser_input(msg, sys_state, cache, key, gui_q)
    elif msg['msg_type'] == 'case_number':
        sys_state = await parse_case_number_request(msg, sys_state, parth, table, gui_q)
    elif msg['msg_type'] == 'archive':
        sys_state = await parse_archive_request(msg, sys_state, cache, key, parth, table, gui_q)
    else:
        print("ux_q item is not valid")
        return None
    return sys_state
    

# start loop that fetches itmes from the input que
async def dequeue_loop(gui_q, ux_q, cache, key, path, table):
    sys_state = memory.get_state_from_cache(cache, key)
    print("DEQUELOOP HAS STARTET")
    counter = 0
    while True:
        try:
            msg = await asyncio.wait_for(ux_q.get(), timeout=1.0)
            # print('msg: ', msg)
            if msg != '400'and isinstance(msg, dict):
                sys_state = await parse_msg(msg, sys_state, cache, key, gui_q, path, table)
                if sys_state:
                    memory.put_state_to_cache(cache, key, sys_state)
        except:
            pass
        current_time = datetime.now()
        sys_state['system']['clock_time'] = current_time.strftime("%H:%M:%S")
        gui_item = oq.create_q_item('system', 'state', sys_state)
        await oq.feed_queue(gui_q, gui_item)

        record_interval = sys_state['system']['autosave']
        if record_interval != 0 and counter % record_interval == 0:
            print(f'TYPE OF CURRENT TIME : {(current_time)}')
            print(f'TYPE OF STARTIME : {(sys_state['system']['start_time'])}')
            sys_state['system']['perfusion_time'] = current_time - sys_state['system']['start_time']
            print('record interval')
            du.execute_entry(path, table, sys_state)
            counter = 0
            print('db entry was executed')
        counter += 1