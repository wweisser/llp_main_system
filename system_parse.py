import db_main as dm
import db_utils as du
import db_to_graph as dtg
import cdi_connect as cdc
import state_utils as su
import memory 
import onque as oq
import db_que as dq
import asyncio
from datetime import datetime

async def parse_serial_input(db_que: dq.Db_Que, msg: dict, sys_state: dict, cc):
    """ditributes msg accoring to the id to parse_cdi, parse_gls... broadcasts the current state"""
    if msg['id'] == 'cdi':
        cdi_arr = cdc.build_cdi_arr(msg['data'])
        sys_state = su.cdi_to_state(sys_state, cdi_arr)
        await oq.broadcast_item('state', 'state', sys_state, cc)
        if sys_state['autosave']:
            db_que.put_db_item('ent', anex='cdi', case_id=sys_state['case_id'], data=cdi_arr)

    elif msg['id'] == 'glm':
        pass
    # memory.put_state_to_cache(cache, key, sys_state)
    return sys_state

async def parse_archive_request(db_que: dq.Db_Que, msg: dict, sys_state: dict):
    if msg['id'] == 'start_record':
        sys_state['autosave'] = True

    elif msg['id'] == 'stop_record':
        sys_state['autosave'] = False

    elif msg['id'] == 'note':
        db_que.put_db_item('ent', anex='note', case_id=sys_state['case_id'], data=msg['data'])

    elif msg['id'] == 'get_data' and isinstance(msg['data'], dict):
        db_que.put_db_item('ext', anex=msg['data']['table'], case_id=sys_state['case_id'], begin=msg['data']['begin'], to=msg['data']['to'], n=msg['data']['n'])

    return sys_state

async def parse_case_number_request(db_que: dq.Db_Que, msg: dict, sys_state: dict, cc, db_path: str, table: str):
    if msg['id'] == 'cn_asgn':
        sys_state['case_id'] = msg['data']
    elif msg['id'] == 'list_request':
        db_que.put_db_item('tlc')
    else:
        pass
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

async def parse_msg(db_que: dq.Db_Que, msg: dict, sys_state, sp, cc):
    # print(f'parse_msg -> Input parser called : {msg}')
    if msg['msg_type'] == 'serial_input':
        sys_state = await parse_serial_input(db_que, msg, sys_state, cc)

    elif msg['msg_type'] == 'case_id':
        sys_state = await parse_case_number_request(db_que, msg, sys_state, cc,)

    elif msg['msg_type'] == 'archive':
        sys_state = await parse_archive_request(msg, sys_state, sp['ux_q'], sp['gui_q'], sp['cache'], sp['key'], sp['db_path'], sp['table'])
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