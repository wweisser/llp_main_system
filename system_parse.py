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

    elif msg['id'] == 'gbm':
        gbm_data = cdc.parse_gbm(msg['data']) 
        print(f'parse_serial_input -> gbm_data {gbm_data}')
    return sys_state

async def parse_archive_request(db_que: dq.Db_Que, msg: dict, sys_state: dict):
    if msg['id'] == 'start_record' and sys_state['case_id'] != 0:
        await db_que.put_db_item(cm_type='stu', case_id=sys_state['case_id'], data=msg['data'])
        sys_state['autosave'] = True
        
    elif msg['id'] == 'stop_record':
        sys_state['autosave'] = False

    elif msg['id'] == 'get_note':
        await db_que.put_db_item('ent', anex='note', case_id=sys_state['case_id'], data=msg['data'])

    elif msg['id'] == 'get_data' and isinstance(msg['data'], dict):
        await db_que.put_db_item('ext', anex=msg['data']['table'], case_id=sys_state['case_id'], begin=msg['data']['begin'], to=msg['data']['to'], n=msg['data']['n'])

    return sys_state

async def parse_case_number_request(db_que: dq.Db_Que, msg: dict, sys_state: dict):
    if msg['id'] == 'cn_asgn':
        sys_state['case_id'] = msg['data']

    elif msg['id'] == 'list_request':
        await db_que.put_db_item('cil')

    return sys_state

async def parse_heartbeat(data, cc):
    if data and isinstance(data, dict) and data['status'] == 'request_handshake':
        data['handshake'] = True
        data['status'] = 'handshake_accepted'
        await oq.broadcast_item('heartbeat', 'bcknd_heartbeat', data, cc)
        print(f'parse_heartbeat -> handshake accapted\n')

async def parse_serial_command():
    pass

async def parse_msg(db_que: dq.Db_Que, msg: dict, sys_state, cc):
    # print(f'parse_msg -> Input parser called : {msg}\n')
    if msg['msg_type'] == 'serial_input':
        sys_state = await parse_serial_input(db_que, msg, sys_state, cc)

    elif msg['msg_type'] == 'archive':
        sys_state = await parse_archive_request(db_que, msg, sys_state)

    elif msg['msg_type'] == 'case_id':
        sys_state = await parse_case_number_request(db_que, msg, sys_state)

    elif msg['msg_type'] == 'system':
        if msg['id'] == 'f_heartbeat':
            await parse_heartbeat(msg['data'], cc)
        elif msg['id'] == 'start_case':
            pass

    else:
        print(f'parse_msg -> invalid command {msg}')
    return sys_state