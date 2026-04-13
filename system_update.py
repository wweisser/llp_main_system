import db_main as dm
import db_utils as du
import db_to_graph as dtg
import cdi_connect as cc
import state_utils as su
import memory 
import onque as oq
import db_to_graph as dbtg
import asyncio
from datetime import datetime

async def parse_serial_input(msg: dict, sys_state: dict, cache, key):
    if msg['id'] == 'cdi':
        sys_state = await parse_cdi_input(msg, sys_state, cache, key)
    return sys_state

async def parse_cdi_input(msg: dict, sys_state: dict, cache, key):
    #is called form deque loop if there is a serial input. Parses the input put it to state and to gui.
    # print(f'parse_cdi_input -> input : {msg['data']}')
    cdi_arr = cc.build_cdi_arr(msg['data'])
    # print(f'parse_cdi_input -> cdi array : {cdi_arr}')
    sys_state = su.cdi_to_state(sys_state, cdi_arr)
    memory.put_state_to_cache(cache, key, sys_state)
    # que_item = oq.create_q_item('system', 'state', sys_state)
    # await oq.feed_queue(gui_q, que_item)
    return sys_state

async def parse_archive_request(msg: dict, sys_state: dict, ux_q, gui_q, cache, key, db_path, table):
    # print('message id : ', msg['id'])
    if msg['id'] == 'start_record':
        sys_state['system']['autosave'] = True
        if sys_state['system']['start_time'] == '0':
            sys_state['system']['start_time'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        record_task = asyncio.create_task(dm.start_case_record(sys_state, ux_q, cache, key))
        if record_task:
            print(f'\nparse_archive_request -> recording has started : {sys_state['system']['start_time']}\n')
            return record_task
    elif msg['id'] == 'stop_record':
        sys_state['system']['autosave'] = False
        print('parse_archive_request -> recording has stoped')
    elif msg['id'] == 'entry':
        await asyncio.to_thread(du.execute_entry(db_path, table, sys_state))
        print('parse_archive_request -> entry request was executed')
    elif msg['id'] == 'data_request':
        pass
    elif msg['id'] == 'graph_data':
        await dtg.create_center_graph_data(db_path, table, gui_q, msg['data'])
    elif msg['id'] == 'change_entry':
        pass
    return sys_state

async def parse_case_number_request(msg: dict, sys_state: dict, gui_q, db_path: str, table: str):
    print('parse_case_number_request -> case_number input parser called')
    if msg['id'] == 'cn_asgn':
        sys_state['system']['case_number'] = msg['data']
        start_time = du.get_val(db_path, table, ['start_time'], 1, sys_state['system']['case_number'])['start_time'][0]
        if start_time and start_time != '0':
            sys_state['system']['start_time'] = start_time
    elif msg['id'] == 'list_request':
        print('\nparse_case_number_request -> Case umber list request received\n')
        val_arr = du.get_all_cn(db_path, table)
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

async def parse_controll_request(msg: dict, sys_state: dict, c):

    return sys_state

async def parse_hub_input(msg: dict, sys_state: dict, com_port_hub: str, tx_q):
    if not com_port_hub:
        com_port_hub = msg['id']
    que_item = oq.create_q_item('hub_request', com_port_hub, msg)
    oq.feed_queue(tx_q, que_item)
    return sys_state

async def parse_msg(msg: dict, sys_state, sp):
    # print(f'Input parser called : {msg}')
    if msg['msg_type'] == 'serial_input':
        # print('parse_msg -> cdi input received')
        sys_state = await parse_serial_input(msg, sys_state, sp['cache'], sp['key'])
    elif msg['msg_type'] == 'hub_input':
        # print('parse_msg -> hub input received')
        sys_state = await parse_hub_input(msg, sys_state)
    elif msg['msg_type'] == 'case_number':
        print('parse_msg -> case number request received')
        print('parse_msg -> arguments to parse casenumber:', sp['gui_q'], sp['db_path'], sp['table'])

        sys_state = await parse_case_number_request(msg, sys_state, sp['gui_q'], sp['db_path'], sp['table'])
    elif msg['msg_type'] == 'archive':
        # print('parse_msg -> archive request received')
        sys_state = await parse_archive_request(msg, sys_state, sp['ux_q'], sp['gui_q'], sp['cache'], sp['key'], sp['db_path'], sp['table'])
    elif msg['msg_type'] == 'entry_request':
        print('parse_msg -> entry request received')
        # sys_state = await parse_note_entry_request(msg, sys_state, sp['gui_q'])
    elif msg['msg_type'] == 'controll':
        # print('parse_msg -> controll request received')
        sys_state = await parse_controll_request(msg, sys_state, sp['com_port_hub'], sp['tx_q'])
    else:
        print(f"parse_msg -> ux_q item is not valid : {msg}")
        return None
    memory.put_state_to_cache(sp['cache'], sp['key'], sys_state)
    return sys_state

# start loop that fetches itmes from the input que
async def dequeue_loop(sp: list, system_tasks):
    sys_state = memory.get_state_from_cache(sp['cache'], sp['key'])
    print("DEQUELOOP HAS STARTED")
    while True:
        try:
            msg = await asyncio.wait_for(sp['ux_q'].get(), timeout=1.0)
            # print('dequeue_loop -> msg: ', msg)
            if msg != '400'and isinstance(msg, dict):
                parse_object = await parse_msg(msg, sys_state, sp)
                if isinstance(parse_object, dict):
                    memory.put_state_to_cache(sp['cache'], sp['key'], parse_object)
                elif isinstance(parse_object, asyncio.Task):
                    system_tasks.append(parse_object)
        except Exception as e:
            print(e)

def calc_time(sys_state, start_time):
    try:
        current_time = datetime.now()
        pt = sys_state['system']['perfusion_time']
        start_time_dt = datetime.strptime(start_time, "%d.%m.%Y %H:%M:%S")
        pt = current_time - start_time_dt
        h, remain = divmod(int(pt.total_seconds()), 3600)
        min, sec = divmod(remain, 60)
        sys_state['system']['perfusion_time'] = f"{h:02}:{min:02}:{sec:02}"    
        return sys_state
    except Exception as e:
        print('gui_updater ->', e)
        return None
    
#calc time fixen

async def gui_updater(cache, key, gui_q, ux_q):
    print('GUI UPDATER STARTED')
    current_time_old = datetime.now()
    counter = 0
    while True:
        current_time = datetime.now()
        sys_state = memory.get_state_from_cache(cache, key)
        sys_state['system']['clock_time'] = current_time.strftime("%H:%M:%S")
        if sys_state['system']['autosave'] and sys_state['system']['start_time'] != 0:
            sys_state = calc_time(sys_state, sys_state['system']['start_time'])
        if sys_state:
            memory.put_state_to_cache(cache, key, sys_state)
        # gui_item = oq.create_q_item('system', 'time', sys_state['system']['clock_time'])
        gui_item = oq.create_q_item('system', 'state', sys_state)
        await oq.feed_queue(gui_q, gui_item)
        if counter > 30:
            if sys_state['system']['case_number'] != 0:
                graph_request = oq.create_q_item('archive', 'graph_data', sys_state['system']['case_number'])
                await oq.feed_queue(ux_q, graph_request)
                print(f'gui_updater -> graph request was send')
            counter = 0
        counter += 1
        await asyncio.sleep(1.0)


