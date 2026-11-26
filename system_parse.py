import ser_utils as sru
import state_utils as su
import onque as oq
import db_que as dq
import asyncio
from datetime import datetime



async def parse_serial_input(db_que: dq.Db_Que, com_q: asyncio.Queue, msg: dict, sys_state: dict, cc):
    print(f'parse_serial_input -> msg: {msg}')
    if msg['id'] == 'cdi':
        sys_state = su.cdi_to_state(sys_state=sys_state, cdi_arr=msg['data'])
        if sys_state['autosave']:
            db_que.put_db_item('ent', anex='cdi', case_id=sys_state['case_id'], data=msg['data'])

    elif msg['id'] == 'gbm':
        sys_state = su.gbm_to_state(sys_state=sys_state, glm_arr=msg['data'])
        # print(f'parse_serial_input -> gbm_data {sys_state['gbm']}')

    if sys_state['gbm']['gbm_align']:
        sys_state = await su.align_gbm(com_q, sys_state)
    #     await sru.send_gbm_command(com_q, sys_state['gbm'])

    await oq.broadcast_item('state', 'state', cc, data=sys_state)

    return sys_state

async def parse_archive_request(db_que: dq.Db_Que, msg: dict, sys_state: dict):
    if msg['id'] == 'get_note':
        await db_que.put_db_item('ent', anex='note', case_id=sys_state['case_id'], data=msg['data'])

    elif msg['id'] == 'get_data' and isinstance(msg['data'], dict):
        await db_que.put_db_item('ext', anex=msg['data']['table'], case_id=sys_state['case_id'], begin=msg['data']['begin'], to=msg['data']['to'], n=msg['data']['n'])

    return sys_state

async def parse_case_number_request(db_que: dq.Db_Que, msg: dict, sys_state: dict, cc):
    if msg['id'] == 'cn_asgn':
        sys_state['case_id'] = msg['data']
        await db_que.put_db_item('ext', anex='start_time', case_id=sys_state['case_id'])
        await oq.broadcast_item('state', 'state', cc, data=sys_state)
        print(f'parse_case_number_request -> case id {msg['data']} asigned')

    elif msg['id'] == 'list_request':
        await db_que.put_db_item('cil')

    return sys_state

async def parse_system_command(db_que: dq.Db_Que, msg: dict, sys_state: dict, cc):
    # print(f'parse_system_command -> msg: {msg}')
    if msg['id'] == 'f_heartbeat':
        await parse_heartbeat(msg['data'], sys_state, cc)

    elif msg['id'] == 'start_time':
        print(f'parse_system_command -> {msg}')
        sys_state['start_time'] = msg['data']['start_time'][0]

    elif msg['id'] == 'start_record':
        sys_state['autosave'] = True
        sys_state['start_time'] = int(datetime.now().timestamp())
        await db_que.put_db_item(cm_type='stu', case_id=sys_state['case_id'], data=sys_state['start_time'])
        await oq.broadcast_item('state', 'state', cc, data=sys_state)
        print(f'parse_system_command -> case was started')
    
    elif msg['id'] == 'stop_record':
        sys_state['autosave'] = False
        await oq.broadcast_item('state', 'state', cc, data=sys_state)

    return sys_state

async def parse_heartbeat(data, sys_state, cc):
    # print(f'parse_heartbeat -> {data}')
    if data and isinstance(data, dict) and data['status'] == 'request_handshake':
        data['handshake'] = True
        data['status'] = 'handshake_accepted'
        await asyncio.sleep(1)

        await oq.broadcast_item('heartbeat', 'bcknd_heartbeat', cc, data=data)
        await asyncio.sleep(1)
        await oq.broadcast_item('state', 'state', cc, data=sys_state)

        print(f'parse_heartbeat -> handshake accapted {data}\n')

async def parse_front_end_command(com_q: asyncio.Queue, msg: dict, sys_state: dict, cc):
    # print(f'parse_front_end_command -> msg: {msg}')
    if msg['id'] == 'switch_align':
        if sys_state['gbm']['gbm_align']: sys_state['gbm']['gbm_align'] = False
        else: sys_state['gbm']['gbm_align'] = True

    elif msg['id'] == 'set_gbm_params':
        sys_state = su.gbm_params_to_state(sys_state, msg['data'])
        if not sys_state['gbm']['gbm_align']:
            await sru.send_gbm_command(com_q, sys_state['gbm'])

        print(f'parse_front_end_command -> gbm command was send {sys_state['gbm']}')

    await oq.broadcast_item('state', 'state', cc, data=sys_state)

    return sys_state

async def parse_msg(db_que: dq.Db_Que, com_q: asyncio.Queue, ux_q: asyncio.Queue, msg: dict, sys_state, cc):
    print(f'')
    if msg['msg_type'] == 'ser_data':
        sys_state = await parse_serial_input(db_que, com_q, msg, sys_state, cc)

    elif msg['msg_type'] == 'archive':
        sys_state = await parse_archive_request(db_que, msg, sys_state)

    elif msg['msg_type'] == 'case_id':
        sys_state = await parse_case_number_request(db_que, msg, sys_state, cc)

    elif msg['msg_type'] == 'system':
        sys_state = await parse_system_command(db_que, msg, sys_state, cc)

    elif msg['msg_type'] == 'front_end_com':
        sys_state = await parse_front_end_command(com_q, msg, sys_state, cc)
    
    else:
        print(f'parse_msg -> invalid command {msg}')
    return sys_state

# Kommunikation backend - frontend Serial -> ux_q -> parse -> cc -> gui_state -> callbacks
# 4 Frontend commando callbacks einführen und Kommunikation testen.