import serial
import serial.tools.list_ports
import asyncio
import cdi_connect as cc
import ser_utils as su
import onque as oq

async def read_serial(serial_port):
    msg = await serial.read(serial_port)
    return msg

def create_portlist():
    active_port_list = []
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        if port.hwid == 'n/a' and "ttyS" in port.device:
            continue
        else:
            active_port_list.append(port)
    return active_port_list

def activate_serial_port(serial_port):
    activ_serial_port = None
    return activ_serial_port

async def serial_connection(serial_port):
    con = activate_serial_port(serial_port)
    msg = await read_serial(serial_port)
    device = su.select_device(msg)
    serial_port.device = device
    while True:
        active_port_list = create_portlist()
        if serial_port not in active_port_list:
            break
        msg = await read_serial(serial_port)
        oq.create_q_item('ser_input', device, msg)
    return con

def connection_handler(tx_q):
    devices = {
        'cdi': {
            'active': False,
            'com_port': None,
            'serial_port': None,
            'last_update': None,
        },
        'hub': {
            'active': False,
            'com_port': None,
            'serial_port': None,
            'last_update': None,
        },
        'g_l_sensor': {
            'active': False,
            'com_port': None,
            'serial_port': None,
            'last_update': None,
        }
    }
    

    
    #update con_arr (erase canceld connection_tasks)
    
    #start tx_q task
    
    #

    pass

# look for connections

# build connections
# read from connections
# -> await first input
# -> determine device


# send input to ux_q

# take form tx_q and ship via serial

# attach to device list

# update device list
# -> check for comports not in the list
# -> if exists create new comport item and attach it to list
# -> if comport on the list that does not exist, cancel it from the list

# delete dead connections

