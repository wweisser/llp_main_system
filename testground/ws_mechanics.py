import asyncio
import serial_asyncio

async def test_reader():
    reader, writer = await serial_asyncio.open_serial_connection(url='COM13', baudrate=9600)
    while True:
        msg = await reader.readline()
        print(f'msg: {msg}')


if __name__ == "__main__":
    asyncio.run(test_reader())
