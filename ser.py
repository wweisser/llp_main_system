import serial
import serial.tools.list_ports
import serial_asyncio
import asyncio
import ser_utils as su
import onque as oq

class Serial_Connection:

    def __init__(self, url, bautrate):
        self.url = url
        self.bautrate = bautrate
        self.reader = None
        self.writer = None
        self.device = None
        self.main_loop = None
        self.ux_loop = None
        self.com_loop = None
        self.active = False
        print(f'2.) building serial port')

    async def open_connection(self, ux_q, com_q):
        try:
            print(f'3.) url={self.url}, baudrate={self.bautrate}')
            self.reader, self.writer = await serial_asyncio.open_serial_connection(url=self.url, baudrate=self.bautrate)
            print(f'3.) serial port {self.url} is open')
            self.active = True

            if self.active == True:
                self.ux_loop = asyncio.create_task(self.run_ux_loop(ux_q))
                # self.com_loop =  asyncio.create_task(self.run_com_loop(com_q))

        except Exception as e:
            'connection was interrupetd'
            self.active = False

    def select_device(self, msg: str):
        if not self.device and isinstance(msg, bytes) and len(msg) > 10:
            i = msg.decode('utf-8')
            print(f'select_device -> indicator chars: {i[1]}, {i[3]}, {i[6]}')
            if (i[1].isdigit() and i[3] == ':' and i[6] == ':'):
                self.device = 'cdi'
                print("cdi detcted")
            elif i[:5] == '<gbm>':
                self.device = 'gbm'
                print("gbm detcted")

    async def run_ux_loop(self, ux_q: asyncio.Queue):
        while self.active:
            msg = None
            # print(f'ux_loop runns for {self.url}, status: {self.active}')
            try:
                # print(f'waiting for msg')
                msg = await self.reader.readline()
                if msg == None:
                    raise ConnectionError(f'{self.url} no connection')
                self.select_device(msg)
                # print(f'received message: {msg}, device: {self.device}')
            except Exception as e:
                print(f'error during serial reading of {self.device}: {e}')
                self.active = False
                break

            await su.dispatch_ser_msg(self.device, msg, ux_q=ux_q)
            # print('msg was dispatched')
            await asyncio.sleep(1)
        print(f'{self.device}-loop was canceled')

async def run_com_loop(com_q: asyncio.Queue, active_ports: list):
    print('com_loop active')
    while True:
        com_item = await com_q.get()
        if isinstance(com_item, dict):
            try:
                for port in active_ports:
                    if port.device == com_item['device']:
                        port.writer.write(com_item['com'].encode("utf-8"))
                        await port.writer.drain()
                print(f'command : {com_item} send\n')
            except:
                port.active = False
                break

async def send_ser_command(com_q: asyncio.Queue, device: str, command: str):
    com_item = {
        'device': device, 
        'com': command
    }
    await com_q.put(com_item)
    print(f'puting item: {com_item}')

def create_portlist():
    active_port_list = []
    port_list = serial.tools.list_ports.comports()
    for port in port_list:
        if port.hwid == 'n/a' and "ttyS" in port.device:
            continue
        else:
            active_port_list.append(port.device)
    return active_port_list


async def serial_connection_manager(ux_q, com_q):
    asyncio.create_task(com_tester(ux_q, com_q))
    print(f'Starting serial_connection_manager\n')
    active_ports = []
    while True:
        port_list = create_portlist() 

        for ap in active_ports:
            if all(ap.url != p for p in port_list) or (ap.device != None and ap.active == False):
                active_ports.remove(ap)
                print(f'removed {ap.url}\n')

        for port in port_list:
            if all(port != ap.url for ap in active_ports):
                np = Serial_Connection(port, 9600)
                np.main_loop = asyncio.create_task(np.open_connection(ux_q, com_q))
                active_ports.append(np)
                print(f'added {np.url}\n')

        await asyncio.sleep(1)

########test########test########test########test########test########test########test########test########test##########

async def com_tester(ux_q: asyncio.Queue, com_q: asyncio.Queue):
    print('starting com_tester')
    # c_0 = 'test'
    # c_I = '<glm>c:0'
    # c_II = '<glm>c:1|21|406;'
    # c_III = '<glm>c:2|214|378;'
    # c_IV = '<glm>c:4'
    # c_V = '<glm>c:9'

    # test_command_arr = [c_0, c_I, c_II, c_III, c_IV, c_V]

    # for c in test_command_arr:
    #     await send_ser_command(com_q, 'gbm', c)

    while True:
        item_from_ux_q = await ux_q.get()
        print(f'q_item: {item_from_ux_q}')

if __name__ == "__main__":

    ux_q = asyncio.Queue()
    com_q = asyncio.Queue()

    try:
        asyncio.run(serial_connection_manager(ux_q, com_q))
    except KeyboardInterrupt:
        pass  # Stilles Beenden – keine Fehlermeldung

########test########test########test########test########test########test########test########test########test##########


# Test 2 komplettieren der programmierung des esp32