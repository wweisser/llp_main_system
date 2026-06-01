import memory 
import onque as oq
import system_parse
import asyncio
from datetime import datetime


# async def parse_note_input(msg: dict, cc, db_path, table, sys_state: dict, now: datetime):
#     # print(f'parse_archive_request -> {now.strftime("%H:%M:%S")}: {msg['data']}\n')
#     if msg['data'] != "" and sys_state['system']['case_number'] != 0:
#         sys_state['notes'] = sys_state['notes'] + f'{now.strftime("%d. %H:%M:%S")}: {msg['data']} \n'
#         note_data = du.get_val(db_path, table, ['notes',] , 800, sys_state['system']['case_number'])
#         archive_note_str = 'n'.join(s for s in note_data['notes'] if s) + '\n'
#         # note_item = oq.create_q_item('notes', 'notes', archive_note_str + sys_state['notes'])
#         # print(f'parse_note_input -> note item time : {note_item['time']}')
#         await oq.broadcast_item('notes', 'notes', archive_note_str + sys_state['notes'], cc)
#     else:
#         # note_item = oq.create_q_item('notes', 'notes', sys_state['notes'])
#         await oq.broadcast_item('notes', 'notes', sys_state['notes'], cc)

#         # print(f'parse_note_input -> note_item : {note_item['time']}')
#     # await oq.feed_queue(cc, note_item)cscs
#     return sys_state

# async def parse_serial_input(msg: dict, sys_state: dict, cache, key):
#     if msg['id'] == 'cdi':
#         print(f'parse_serial_input-> {msg}')
#         sys_state = await parse_cdi_input(msg, sys_state, cache, key)
#     return sys_state

# async def parse_cdi_input(msg: dict, sys_state: dict, cache, key):
#     cdi_arr = cc.build_cdi_arr(msg['data'])
#     # print(f'parse_cdi_input -> {cdi_arr}')
#     sys_state = su.cdi_to_state(sys_state, cdi_arr)
#     memory.put_state_to_cache(cache, key, sys_state)
#     return sys_state

# async def parse_archive_request(msg: dict, sys_state: dict, ux_q, cc, cache, key, db_path, table):
#     # print('message id : ', msg['id'])
#     now = datetime.now()
#     if msg['id'] == 'start_record':
#         sys_state['system']['autosave'] = True
#         if sys_state['system']['start_time'] == 0:
#             sys_state['system']['start_time'] = now.strftime("%d.%m.%Y %H:%M:%S")
#         record_task = asyncio.create_task(dm.start_case_record(sys_state, ux_q, cache, key))
#         if record_task:
#             print(f'\nparse_archive_request -> recording has started : {sys_state['system']['start_time']}\n')
#             return record_task
#     elif msg['id'] == 'stop_record':
#         sys_state['system']['autosave'] = False
#         print('parse_archive_request -> recording has stoped')
#     elif msg['id'] == 'entry':
#         await asyncio.to_thread(du.execute_entry(db_path, table, msg['data']))
#         print('parse_archive_request -> entry request was executed')
#         sys_state['notes'] == ''
#     elif msg['id'] == 'note_entry':
#             sys_state = await parse_note_input(msg, cc, db_path, table, sys_state, now)
#     elif msg['id'] == 'event_entry':
#         sys_state['events'].append(msg['data'])
#     elif msg['id'] == 'change_entry':
#         pass
#     elif msg['id'] == 'data_request':
#         pass
#     elif msg['id'] == 'graph_data':
#         await dtg.create_center_graph_data(db_path, table, cc, msg['data'])
#         # sys_state['notes'] = sys_state['notes'].append(msg['data'])
#     return sys_state

# async def parse_case_number_request(msg: dict, sys_state: dict, cc, db_path: str, table: str):
#     print('parse_case_number_request -> case_number input parser called')
#     if msg['id'] == 'cn_asgn':
#         sys_state['system']['case_number'] = msg['data']
#         start_time = du.get_val(db_path, table, ['start_time'], 1, sys_state['system']['case_number'])['start_time'][0]
#         if start_time and start_time != 0:
#             sys_state['system']['start_time'] = start_time
#         else:
#             sys_state['system']['start_time'] = 0
#     elif msg['id'] == 'list_request':
#         print('\nparse_case_number_request -> Case umber list request received\n')
#         val_arr = du.get_all_cn(db_path, table)
#         if val_arr:
#             await oq.broadcast_item('case_number', 'cn_list', val_arr, cc)
#             # que_item = oq.create_q_item
#             # await oq.feed_queue(cc, que_item)
#             print('parse_case_number_request -> list que item was created und fed to gui que : \n', val_arr, '\n')
#     elif msg['id'] == 'start_perfusion':
#             sys_state['system']['autosave'] = True
#             print(f'parse_case_number_request -> Autosave interval is set to {msg['data']} in sys_state to \n')
#     else:
#         pass
#     return sys_state

# async def parse_controll_request(msg: dict, sys_state: dict, c):

#     return sys_state

# async def parse_hub_input(msg: dict, sys_state: dict, com_port_hub: str, tx_q):
#     if not com_port_hub:
#         com_port_hub = msg['id']
#     # que_item = oq.create_q_item('hub_request', com_port_hub, msg)
#     # oq.feed_queue(tx_q, que_item)
#     await oq.broadcast_item('hub_request', com_port_hub, msg, cc)

#     return sys_state

# async def parse_msg(msg: dict, sys_state, sp):
#     # print(f'Input parser called : {msg}')
#     if msg['msg_type'] == 'serial_input':
#         sys_state = await parse_serial_input(msg, sys_state, sp['cache'], sp['key'])
#     elif msg['msg_type'] == 'hub_input':
#         sys_state = await parse_hub_input(msg, sys_state)
#     elif msg['msg_type'] == 'case_number':
#         sys_state = await parse_case_number_request(msg, sys_state, sp['gui_q'], sp['db_path'], sp['table'])
#     elif msg['msg_type'] == 'archive':
#         sys_state = await parse_archive_request(msg, sys_state, sp['ux_q'], sp['gui_q'], sp['cache'], sp['key'], sp['db_path'], sp['table'])
#     elif msg['msg_type'] == 'entry_request':
#         print('parse_msg -> entry request received')
#         # sys_state = await parse_note_entry_request(msg, sys_state, sp['gui_q'])
#     elif msg['msg_type'] == 'controll':
#         # print('parse_msg -> controll request received')
#         sys_state = await parse_controll_request(msg, sys_state, sp['com_port_hub'], sp['tx_q'])
#     elif msg['msg_type'] == 'system' and msg['id'] == 'refresh_gui' and sys_state['system']['case_number'] != 0:
#         print('parse_msg -> refresh_gui')
#         # graph_item = oq.create_q_item('archive', 'graph_data', sys_state['system']['case_number'])
#         # note_item = oq.create_q_item('archive', 'note_entry', '!')
#         # await asyncio.sleep(0.5)
#         # await oq.feed_queue(sp['ux_q'], graph_item)
#         # await asyncio.sleep(0.5)
#         # await oq.feed_queue(sp['ux_q'], note_item)
#         await oq.broadcast_item('archive', 'graph_data', sys_state['system']['case_number'], cc)
#         await oq.broadcast_item('archive', 'note_entry', '!', cc)
#     else:
#         print(f"parse_msg -> ux_q item is not valid : {msg}")
#         return None
#     memory.put_state_to_cache(sp['cache'], sp['key'], sys_state)
#     return sys_state

def generate_one_beat(last_heartbeat: str, status: str):
    b_heartbeat = {
        'last_heartbeat': last_heartbeat,
        'status': status,
    }
    return b_heartbeat

def genertate_graph_output():
    pass

# start loop that fetches itmes from the input que
async def dequeue_loop(sp: list, system_tasks: list, cc):
    sys_state = memory.get_state_from_cache(sp['cache'], sp['key'])
    print("DEQUELOOP STARTED")
    while True:
        try:
            # msg = await asyncio.wait_for(sp['ux_q'].get(), timeout=1.0)
            msg = await sp['ux_q'].get()
            # print('dequeue_loop -> msg: ', msg)
            if msg != '400'and isinstance(msg, dict):
                parse_object = await system_parse.parse_msg(msg, sys_state, sp, cc)
                if isinstance(parse_object, dict):
                    memory.put_state_to_cache(sp['cache'], sp['key'], parse_object)
                elif isinstance(parse_object, asyncio.Task):
                    system_tasks.append(parse_object)
        except Exception as e:
            print(e)

def calc_perfusion_time(sys_state, start_time):
    try:
        current_time = datetime.now()
        pt = sys_state['system']['perfusion_time']
        start_time_dt = datetime.strptime(start_time, "%d.%m.%Y %H:%M:%S")
        pt = current_time - start_time_dt
        h, remain = divmod(int(pt.total_seconds()), 3600)
        min, sec = divmod(remain, 60)
        sys_state['system']['perfusion_time'] = f"{h:02}:{min:02}:{sec:02}" 
        # print(f'calc_time -> pefusion time : {sys_state['system']['perfusion_time']}')
        return sys_state
    except Exception as e:
        print('gui_updater ->', e)
        return None

async def b_heartbeat(cc):
    print('BACKEND HEARTBEAT STARTED')
    while True:
        ct = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        b_heartbeat_item = generate_one_beat(ct, "backend_active")
        await oq.broadcast_item('system', 'state', b_heartbeat_item, cc)

async def system_updater(cache, key, archive_intervall: int, update_intervall: float):
    """System updater loop that updates the system state every second.
    Perfusion time and clock time and archive funktion"""
    counter = 0
    while True:
        ct = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys_state = memory.get_state_from_cache(cache, key)
        if sys_state and ct:
            sys_state['system']['clock_time'] = ct

        if sys_state['system']['autosave'] and sys_state['system']['start_time'] != 0:
            sys_state = calc_perfusion_time(sys_state, sys_state['system']['start_time'])
            memory.put_state_to_cache(cache, key, sys_state)

        if counter > archive_intervall:
            counter = 0
        counter += 1
        await asyncio.sleep(update_intervall)
