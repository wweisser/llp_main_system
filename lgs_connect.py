# -*- coding: utf-8 -*-

"""This simple script reads data from a COM port, to which a SIX Potentiostat is
#connected. Then it stores the timestamp in s, the current in nA and the temperature in degree C in a tab-delimited txt file.

The SIX potentiotat delivers a data point every 1.7 seconds, which is shown on
screen and stored a tab-delimited txt file:
Timestamp in s
ch1 current in nA
ch2 current in nA
ch3 current in nA
ch4 current in nA
ch5 current in nA
ch6 current in nA
Temperature in °C

Start conditions:
SIX potentiostat is connected to a known COM port
- output file name
"""
import serial
import time

# Input data:
# COM_PORT = "COM5" # This needs to be changed accordingly
OUT_FILENAME = "out_data.txt" # This needs to be changed accordingly

# # Serial port settings
# BAUD = 9600
# TIMEOUT = 0.5

# Data telegram settings
package_length = 25 # the SIX potentiostat delivers 25-bytes messages
data_block = [b'\x00'] * package_length # ring array for incomming data
start_timestamp = None

# Starting serial port connection
# with serial.Serial(COM_PORT, baudrate=BAUD, timeout=TIMEOUT) as ser, open(OUT_FILENAME, 'w') as file:
# output first line
first_line = "Time/s\tCh1/nA\tCh2/nA\tCh3/nA\tCh4/nA\tCh5/nA\tCh6/nA\tT/°C"
print(first_line)
# file.write(first_line + "\n")
ser = "FILL IN SERIAL PORT HERE"
while(1): # Script will run until Ctrl+Z or Ctrl+C is pressed
# Read data from serial port if available in the input buffer
    data = None
    if ser.inWaiting(): # is data in input buffer?
        data = ser.read()
    if data is not None:
        # operating with a ring array of size 25.
        # data is inserted at 0 and removed at 25. Therefore,
        # the data is inverted order in the array.
        # array ==> [newest_byte .... oldest_byte]
        # Each time the code parses the ring array is parsed until
        # a valid telegram is recognized.
        data_block.insert(0, data) # last byte in position 0
        nirvana = data_block.pop()
        del(nirvana) # position 26 is deleted
        header = [b'\x04', b'\x68', b'\x13', b'\x13', b'\x68']
        # Telegram header (inverted) see documentation
        cks = 0 # checksum
        # calculating checksum from byte 4 till second to last byte
        for x in [int.from_bytes(x, 'big') for x in data_block[2:-4]]:
            cks = (cks + x) & 0xFF
        # validating header, end byte (x16) and checksum
        if data_block[-5:] == header and data_block[0] == b'\x16' and int.from_bytes(data_block[1], 'big') == cks:
        # now inverting data train
        # Useful data are from byte 5 until second to last byte.
            data_inv = [x for x in data_block[2:-5]]
            data_inv.reverse()
            it = iter(data_inv) # iterator used to fetch 2 bytes
            # next line turns 2 bytes into a 16-bit integer array
            out_data = [int.from_bytes(b''.join([x, next(it)]), byteorder='big', signed=True) for x in it]
            # data to be stored
            to_save = [str(x) for x in out_data] # 16-bit signed integers
            # converting input data to currents in nanoamperes
            # 50 nA ==> 32767 (2^15-1)
            # applying gain and updating data as nanoamp.
            gain = 50 / (2**15 - 1)
            to_insert = [str(round(int(x) * gain, 3)) for x in to_save[0:6]]
            # converting temperature to °C
            temperature = str(round(float(to_save[6]) / 16, 3))
            to_insert.append(temperature)
            # generating timestamps
            timestamp = round(time.time(), 4)
            if start_timestamp is None:
                start_timestamp = timestamp
                delta_time = 0
            else:
                delta_time = timestamp - start_timestamp
                to_insert.insert(0, str(round(delta_time, 1)))
            # printing data on screen and output file
            print("\t".join(to_insert))
            file.write("\t".join(to_insert) + "\n")
            # Next data point arrives in about 1.6 seconds
            # So, resting for 1.4 seconds should be enough 