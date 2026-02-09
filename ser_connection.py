import serial
import serial.tools.list_ports
import asyncio
import cdi_connect as cc
import ser_utils as su
import onque as oq

class serial_connection:
    def __init__(self, comport, serial_port, read_task):
        self.comport = comport
        self.serial_port = serial_port
        self.read_task = read_task
    
    def get_state_of_task(self):
        """checks for the state of a read task, returns 'active', if intact an running"""
        if self.read_task.done():
            return 'done'
        elif self.read_task.cancelled():
            return 'cancelled'
        else:
            return 'active'

    def state_serial_port(self):
        """checks for the state of a serial connection, returen 'open', 'closed' or None in the event of an error"""
        try:
            ser_is_open = self.serial_port.is_open
            if ser_is_open:
                return 'open'
            elif not ser_is_open:
                return 'closed'
        except:
            return None

def create_con(port, ux_q):
    """Takes a port and cerates a serial_connection object and returns it. 
    In the event of an error None is returned"""
    try:
        ser = serial.Serial(port.device, 9600, 8, "N", 1, timeout=6.0)
    except Exception as e:
        ser = None
        print(f"serial port for {port.device} could not be created\n", e)
    try:
        if ser:
            read_task = asyncio.create_task(read_ser(ser, ux_q))
            con = serial_connection(port.device, ser, read_task)
            return con
    except Exception as e:
        print(f"read task for {port.device} could not be created\n", e)
    return None
    
def create_con_arr(ux_q):
    """Creates a serial_connection object for every port in the port_list"""
    port_list = serial.tools.list_ports.comports()
    connections_arr = []
    for port in port_list:
        con = create_con(port, ux_q)
        if con:
            connections_arr.append(con)
    return connections_arr

def check_con(con):
    """Takes a serial_connection object and checks the state of the serial connection and the read task.
    Returns 'active' or 'connection_dead' or 'read_task_dead'"""
    ser_port_open = con.state_serial_port()
    read_task_active = con.get_state_of_task()
    if ser_port_open != 'open':
        return 'connection_dead'
    elif read_task_active != 'active':
        return 'read_task_dead'
    else:
        return 'active'

def check_for_new_con(con_arr, ux_q):
    """Aligns the serial_connection array with the port_list.
    Creates a new serial_connection object and adds it con_arr. Con_arr is then returend """
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        port_present = False
        for con in con_arr:
            if port.device == con.comport:
                port_present = True
        if not port_present:
            con = create_con(port, ux_q)
            if con:
                con_arr.append(con)
    return con_arr

def check_for_dead_con(con_arr, ux_q):
    """Discards dead serial_connection objects or restarts the read tasks.
    The con_arr is returned"""
    if con_arr != []:
        to_remove = []
        for con in con_arr:
            state_of_con = check_con(con)
            if state_of_con == 'read_task_dead':
                print(f'connection to {con.comport} has died')
                to_remove.append(con)
        for con in to_remove:
            con_arr.remove(con)
    return con_arr

#Disconnetion handler for serial devices
def input_to_q_item(buffer):
    device = su.select_device(buffer)
    ser_input = ""
    if device == 'cdi':
        ser_input = buffer.decode('utf-8')
    q_item = oq.create_q_item('ser_input', device, ser_input)
    return q_item

async def read_ser(ser, ux_q):
    loop = asyncio.get_event_loop()
    buffer = ''
    while True:
        if ser and ser.is_open:
            try:
                buffer = await loop.run_in_executor(None, ser.readline)
                if buffer != b'' and buffer != "":
                    # print(buffer)
                    q_item = input_to_q_item(buffer)
                    await oq.feed_queue(ux_q, q_item)
            except Exception as e:
                print(f'read task cancelled on {ser.port}')
                break

async def check_con_state(con_arr, ux_q):
    while True:
        con_arr = check_for_new_con(con_arr, ux_q)
        con_arr = check_for_dead_con(con_arr, ux_q)
        try:
            await asyncio.sleep(1)
        except:
            print("check_con_state was cancelled during sleep")
            raise

async def connection_handler(ux_q):
    con_arr = create_con_arr(ux_q)
    try:
        await check_con_state(con_arr, ux_q)
    except:
        print("connection handler crashed")
        raise

if __name__ == '__main__':
    ux_q = None
    try:
        task = asyncio.run(connection_handler(ux_q))
    except KeyboardInterrupt:
        print('keyboard interupt')


