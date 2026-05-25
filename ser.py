import serial
import serial.tools.list_ports
import serial_asyncio
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
    # print(f'create_portlist -> {active_port_list}')
    return active_port_list

async def serial_connection(port, device_state, ux_q):
    try:
        reader, writer = await serial_asyncio.open_serial_connection(url=port, baudrate=9600)
        # serial_port = serial.Serial(com_port, 9600, 8, "N", 1, timeout=1.0)
        print(f'serial_connection -> serial_connection created')
    except Exception as e:
        print(f"{datetime.now()} serial_connection -> serial port to {port} could not be created")
        print(e)
        return None
    msg = await read_serial(reader)
    while not msg:
        msg = await read_serial(reader)
    device = su.select_device(msg)
    print(f'serial_connection -> message : { msg}\n device : {device} detcted\n')
    if device:
        device_state['active'][device] = True
        device_state['last_update'][device] = datetime.now()
        device_state['reader'][device] = reader
        device_state['writer'][device] = writer
    else:
        return None
    while True:
        active_port_list = create_portlist()
        if port not in active_port_list:
            device_state['active'][device] = False
            device_state['comports'][device] = None
            device_state['serial_port'][device] = None
            device_state['last_update'][device] = datetime.now()
            print(f"{datetime.now()} serial_connection -> {device} disconected, last update : {device_state['last_update'][device]}")
            return
        msg = await read_serial(reader)
        device_state['last_update'][device] = datetime.now()
        if msg:
            q_item = oq.create_q_item('serial_input', device, msg)
            print(f'serial_connection ->  {q_item}')
            await oq.feed_queue(ux_q, q_item)
        await asyncio.sleep(1)
        

            

async def update_device_state(device_state, ux_q):
    print(f'{datetime.now()} update_device_state -> task was started')
    while True:
        active_port_list = create_portlist()
        print(f'update_device_state -> {active_port_list}', device_state['connecting_ports'])
        for port in active_port_list:
            if not port in list(device_state['connecting_ports']):
                device_state['connecting_ports'].append(port)
                asyncio.create_task(serial_connection(port, device_state, ux_q))
        for port in list(device_state['connecting_ports']): 
            if port not in active_port_list:
                device_state['connecting_ports'].remove(port)
        await asyncio.sleep(1)

async def read_serial(reader):
    try:
        # msg = await loop.run_in_executor(None, serial_port.readline)
        line = await reader.readline() 
        if line:
            # print(f'read_serial -> {line}')
            return line
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
        },
        'reader':{
            'hub': None,
            'cdi': None,
            'g_l': None,
            'hsi': None,
        },
        'writer':{
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