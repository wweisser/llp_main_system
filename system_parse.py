import ser
import state_utils as su
import onque as oq
import db_que as dq
import asyncio



async def parse_serial_input(db_que: dq.Db_Que, com_q: asyncio.Queue, msg: dict, sys_state: dict, cc):
    print(f'parse_serial_input -> msg: {msg}')
    if msg['id'] == 'cdi':
        sys_state = su.cdi_to_state(sys_state=sys_state, cdi_arr=msg['data'])
        # if sys_state['autosave']:
        #     db_que.put_db_item('ent', anex='cdi', case_id=sys_state['case_id'], data=msg['data'])

    elif msg['id'] == 'gbm':
        sys_state = su.gbm_to_state(sys_state=sys_state, glm_arr=msg['data'])
        print(f'parse_serial_input -> gbm_data {msg['data']}')

    if sys_state['gbm_align']:
        sys_state = await su.align_gbm(com_q, sys_state)

    await oq.broadcast_item('state', 'state', cc, data=sys_state)


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
        await oq.broadcast_item('heartbeat', 'bcknd_heartbeat', cc, data=data)
        print(f'parse_heartbeat -> handshake accapted\n')

async def parse_front_end_command(com_q: asyncio.Queue, msg: dict):
    # command to serial device
    ser.send_ser_command(com_q = com_q, device = msg['id'], command = msg['data'])
    # command to system like on and off of automation


async def parse_msg(db_que: dq.Db_Que, com_q: asyncio.Queue, ux_q: asyncio.Queue, msg: dict, sys_state, cc):
    if msg['msg_type'] == 'ser_data':
        sys_state = await parse_serial_input(db_que, com_q, msg, sys_state, cc)

    elif msg['msg_type'] == 'archive':
        sys_state = await parse_archive_request(db_que, msg, sys_state)

    elif msg['msg_type'] == 'case_id':
        sys_state = await parse_case_number_request(db_que, msg, sys_state)

    elif msg['msg_type'] == 'system':
        if msg['id'] == 'f_heartbeat':
            await parse_heartbeat(msg['data'], cc)
        elif msg['id'] == 'start_case':
            pass

    elif msg['msg_type'] == 'serial_commmand':
        parse_front_end_command(com_q, msg)
    
    else:
        print(f'parse_msg -> invalid command {msg}')
    return sys_state


# Kommunikation backend - frontend Serial -> ux_q -> parse -> cc -> gui_state -> callbacks
# 4 Frontend commando callbacks einführen und Kommunikation testen.