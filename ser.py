import serial
import serial.tools.list_ports
import asyncio
import ser_utils as su
import onque as oq
from datetime import datetime

def create_portlist():
    active_port_list = []
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        if port.hwid == 'n/a' and "ttyS" in port.device:
            continue
        else:
            active_port_list.append(port.device)
    return active_port_list

async def serial_connection(com_port, device_state, ux_q):
    try:
        serial_port = serial.Serial(com_port, 9600, 8, "N", 1, timeout=1.0)
    except Exception as e:
        print(f"{datetime.now()} serial_connection -> serial port to {com_port} could not be created")
        print(e)
        return None
    msg = await read_serial(serial_port)
    device = su.select_device(msg)
    if device:
        device_state['active'][device] = True
        device_state['comports'][device] = serial_port.device
        device_state['serial_port'][device] = serial_port
        device_state['last_update'][device] = datetime.now()
    else:
        return None
    while True:
        active_port_list = create_portlist()
        if com_port not in active_port_list:
            device_state['active'][device] = False
            device_state['comports'][device] = None
            device_state['serial_port'][device] = None
            device_state['last_update'][device] = datetime.now()
            print(f"{datetime.now()} serial_connection -> {device} disconected, last update : {device_state['last_update'][device]}")
            break
        msg = await read_serial(serial_port)
        device_state['last_update'][device] = datetime.now()
        if msg:
            q_item = oq.create_q_item('serial_input', device, msg)
            oq.feed_queue(ux_q, q_item)

async def update_device_state(device_state, ux_q):
    print(f'{datetime.now()} update_device_state -> task was started')
    while True:
        active_port_list = create_portlist()
        for port in active_port_list:
            if not port in device_state['connecting_ports']:
                device_state['connecting_ports'].append(port)
                asyncio.create_task(serial_connection(port, device_state, ux_q))
        for port in list(device_state['connecting_ports']): 
            if port in device_state['comports'].values():
                device_state['connecting_ports'].remove(port)
        await asyncio.sleep(1)

async def read_serial(serial_port):
    try:
        loop = asyncio.get_running_loop()
        if not serial_port.is_open:
            serial_port.open()
        msg = await loop.run_in_executor(None, serial_port.readline)
        if msg:
            return msg
    except Exception as e:
        print(f"{datetime.now()} read_serial -> could not read from serial port")
        print(e)

async def send_serial_task(device_state, tx_q):
    print(f'{datetime.now()} send_serial -> task was started')
    while True:
        msg = await tx_q.get()
        hub_port = device_state['serial_port']['hub']
        if not device_state['active']['hub'] or not hub_port:
            print(f'{datetime.now()} send_serial -> Message {msg} could not be send')
            continue
        try:
            if msg and isinstance(msg, str):
                if not hub_port.is_open:
                    hub_port.open()
                hub_port.write(msg.encode())
        except Exception as e:
            print(f'{datetime.now()} send_serial -> message could not be send')

async def connection_handler(tx_q, ux_q):
    device_state = {
        'connecting_ports': [],
        'active': {
            'cdi': False,
            'hub': False,
            'hsi': False,
            'g_l': False,
        },
        'comports': {
            'hub': None,
            'cdi': None,
            'g_l': None,
            'hsi': None,
        },
        'serial_port': {
            'hub': None,
            'cdi': None,
            'g_l': None,
            'hsi': None,
        },
        'last_update':{
            'hub': None,
            'cdi': None,
            'g_l': None,
            'hsi': None,
        }
    }
    await asyncio.gather(
        asyncio.create_task(send_serial_task(device_state, tx_q)),
        asyncio.create_task(update_device_state(device_state, ux_q))
    )


if __name__ == "__main__":
    ux_q = asyncio.Queue()
    tx_q = asyncio.Queue()
    try:
        asyncio.run(connection_handler(tx_q, ux_q))
    except KeyboardInterrupt:
        pass  # Stilles Beenden – keine Fehlermeldung