import db_main as dm
import db_utils as du
import db_to_graph as dtg
import cdi_connect as cc
import state_utils as su
import memory 
import onque as oq
import db
import asyncio
from datetime import datetime

async def parse_note_input(msg: dict, cc, db_path, table, sys_state: dict, now: datetime):
    # print(f'parse_archive_request -> {now.strftime("%H:%M:%S")}: {msg['data']}\n')
    if msg['data'] != "" and sys_state['system']['case_number'] != 0:
        sys_state['notes'] = sys_state['notes'] + f'{now.strftime("%d. %H:%M:%S")}: {msg['data']} \n'
        note_data = du.get_val(db_path, table, ['notes',] , 800, sys_state['system']['case_number'])
        archive_note_str = 'n'.join(s for s in note_data['notes'] if s) + '\n'
        # note_item = oq.create_q_item('notes', 'notes', archive_note_str + sys_state['notes'])
        # print(f'parse_note_input -> note item time : {note_item['time']}')
        await oq.broadcast_item('notes', 'notes', archive_note_str + sys_state['notes'], cc)
    else:
        # note_item = oq.create_q_item('notes', 'notes', sys_state['notes'])
        await oq.broadcast_item('notes', 'notes', sys_state['notes'], cc)

        # print(f'parse_note_input -> note_item : {note_item['time']}')
    # await oq.feed_queue(cc, note_item)cscs
    return sys_state

async def parse_cdi_input(msg: dict, sys_state: dict):
    """Calls build_cdi_arr and cdi_to_state, sends an achrive request for entry in the cdi_table (not ready)"""
    cdi_arr = cc.build_cdi_arr(msg['data'])
    sys_state = su.cdi_to_state(sys_state, cdi_arr)
    return 

async def parse_gls_input(msg: dict, sys_state: dict):
    """Parses input from gls and puts it to state, sends an achrive request for entry in the gls_table (not ready)"""
    return sys_state

async def parse_serial_input(msg: dict, sys_state: dict, cache, key, cc):
    """ditributes msg accoring to the id to parse_cdi, parse_gls... broadcasts the current state"""
    if msg['id'] == 'cdi':
        sys_state = await parse_cdi_input(msg, sys_state)
        await oq.broadcast_item('state', 'state', sys_state, cc)
    elif msg['id'] == 'gls':
        pass
    memory.put_state_to_cache(cache, key, sys_state)
    return sys_state

async def parse_archive_request(msg: dict, sys_state: dict, ux_q, cc, cache, key, db_path, table):
    # print('message id : ', msg['id'])
    now = int(datetime.now().timestamp()),
    if msg['id'] == 'start_record':
        # call dbt-create_case 
        sys_state['system']['autosave'] = True
        if sys_state['system']['start_time'] == 0:
            sys_state['system']['start_time'] = now.strftime("%d.%m.%Y %H:%M:%S")
        record_task = asyncio.create_task(dm.start_case_record(sys_state, ux_q, cache, key))
        if record_task:
            print(f'\nparse_archive_request -> recording has started : {sys_state['system']['start_time']}\n')
            return record_task
    elif msg['id'] == 'stop_record':
        sys_state['system']['autosave'] = False
        print('parse_archive_request -> recording has stoped')
    elif msg['id'] == 'entry':
        # create options for every table and call the adjasoned funktion
        await asyncio.to_thread(du.execute_entry(db_path, table, msg['data']))
        print('parse_archive_request -> entry request was executed')
        sys_state['notes'] == ''
    elif msg['id'] == 'note_entry':
        #see above
        sys_state = await parse_note_input(msg, cc, db_path, table, sys_state, now)
    elif msg['id'] == 'get_cn_list':
        pass
    elif msg['id'] == 'get_data':
        # in the data package of the msg there need to be a dict {'cn': <cn>, 'params': [<list>], 'begin': <begin>, 'to':<end>}
        # then inspect table musst be called and the data musst be parse like with get_case_data
        pass
    elif msg['id'] == 'graph_data':
        # In the data package of the msg there need to be a dict {'cn': <cn>, 'params': [<list>], 'begin': <begin>, 'to':<end>}
        # Then data needs to be made graph ready
        await dtg.create_center_graph_data(db_path, table, cc, msg['data'])
    return sys_state

async def parse_case_number_request(msg: dict, sys_state: dict, cc, db_path: str, table: str):
    print('parse_case_number_request -> case_number input parser called')
    if msg['id'] == 'cn_asgn':
        # sends request for starttime to archive
        sys_state['system']['case_number'] = msg['data']
    elif msg['id'] == 'list_request':
        print('\nparse_case_number_request -> Case umber list request received\n')
        # needs to be reditected to archive
        val_arr = du.get_all_cn(db_path, table)
        if val_arr:
            await oq.broadcast_item('case_number', 'cn_list', val_arr, cc)
    elif msg['id'] == 'start_perfusion':
        # Needs also to be redirected to archive. If there is no case in cases, one needs to be created.
        sys_state['system']['autosave'] = True
        print(f'parse_case_number_request -> Autosave interval is set to {msg['data']} in sys_state to \n')
    else:
        pass
    return sys_state

async def parse_controll_request(msg: dict, sys_state: dict, comport_hub, tx_q):
    return sys_state

async def parse_heartbeat(msg: dict, cc):
    print(f'parse_msg -> heartbeat from {msg['last_heartbeat']} received, startup ckeck: {msg['startup_check']}, status: {msg['status']}\n')
    if msg['startup_check'] and msg['status'] == 'request_handshake':
        b_heartbeat_item = {
            'last_heartbeat': int(datetime.now().timestamp()),
            'status': 'handshake_accepted',
            'error_state': None,
        }
        await oq.broadcast_item('heartbeat', 'b_heartbeat', b_heartbeat_item, cc)


async def parse_msg(msg: dict, sys_state, sp, cc):
    # print(f'parse_msg -> Input parser called : {msg}')
    if msg['msg_type'] == 'serial_input':
        sys_state = await parse_serial_input(msg, sys_state, sp['cache'], sp['key'], cc)
    elif msg['msg_type'] == 'case_number':
        sys_state = await parse_case_number_request(msg, sys_state, cc, sp['db_path'], sp['table'])
    elif msg['msg_type'] == 'archive':
        sys_state = await parse_archive_request(msg, sys_state, sp['ux_q'], sp['gui_q'], sp['cache'], sp['key'], sp['db_path'], sp['table'])
    elif msg['msg_type'] == 'controll':
        # print('parse_msg -> controll request received')
        sys_state = await parse_controll_request(msg, sys_state, sp['com_port_hub'], sp['tx_q'])
    elif msg['msg_type'] == 'system':
        if msg['id'] == 'refresh_gui' and sys_state['system']['case_number'] != 0:
            print('parse_msg -> refresh_gui')
        elif msg['id'] == 'f_heartbeat':
            await parse_heartbeat(msg['data'], cc)
    else:
        print(f"parse_msg -> ux_q item is not valid : {msg}")
        return None
    memory.put_state_to_cache(sp['cache'], sp['key'], sys_state)
    return sys_state