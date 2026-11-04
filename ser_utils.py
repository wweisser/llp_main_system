import onque as oq


# "<gbm>m:state|" + set_fio2 + "|" + set_total_flow + "|" + set_oxygen_flow + "|" + set_air_flow + "|" + fio2 + "|" + oxygen_flow + "|" + air_flow;

def process_cdi_msg(msg):
    i = 0
    cdi_arr = []
    l = len(msg)

    while i < l:
        
        if(msg[i] == '\t'):
            numb_var = None
            sign = 1
            dec = 1
            i += 1
            while not (i >= l or msg[i] == '\t'):

                if msg[i] == '-' and msg[i+1].isdigit():
                    sign *= -1

                if numb_var == None and msg[i].isdigit():
                    numb_var = int(msg[i])

                elif numb_var and msg[i].isdigit():
                    numb_var = numb_var* 10 + int(msg[i])

                if numb_var and msg[i] == '.' and msg[i+2].isdigit():
                    dec = 0.01

                elif numb_var and msg[i] == '.' :
                    dec = 0.1

                i += 1
            if numb_var:
                numb_var = round((numb_var*sign*dec), 2)
            cdi_arr.append(numb_var)
        else:
            i += 1
    return cdi_arr

def process_gbm(msg: str) -> list:
    arr = []
    l = len(msg)
    i = 0
    while i < l:
        if msg[i] == '|' and i < l:
            i += 1
            numb = 0
            while i < l and msg[i].isdigit():
                numb = numb * 10 + int(msg[i])
                i += 1
            arr.append(numb)
        else:
            i += 1
    return arr
            
async def dispatch_ser_msg(device:str, msg: str, ux_q):
    if msg:
        if isinstance(msg, bytes):
            msg = msg.decode("utf-8")

        if device == 'cdi':
            serial_data = process_cdi_msg(msg)
        elif device == 'gbm':
            serial_data = process_gbm(msg)

        if serial_data != []:
            await oq.feed_q(ux_q, 'ser_data', device, serial_data)



    

# if __name__ == '__main__':
#     import asyncio
#     #           Time      pH   CO2   O2    Temp  HCO3  BE    cSO2  K+    VO2   Q     BSA   pH    CO2   O2    Temp  SO2   HCT   HGB
#     #         b' 18:40:34\t7.14\t ---\t ---\t33.9\t -- \t -- \t ---\t -.-\t ---\t -.-\t    \t7.30\t ---\t ---\t33.4\t ---\t ---\t -.-\r\n'
#     test =  b' 09:41:33\t7.14\t ---\t ---\t-26.4\t --\t --\t ---\t -.-\t ---\t -.-\t    \t7.26\t ---\t ---\t25.5\t ---\t 25%\t  -.-\r\n'
#     print(test)
#     ux_q = asyncio.Queue()
#     com_q = asyncio.Queue()

#     arr = asyncio.run(dispatch_ser_msg('cdi', test, com_q))
#     print(arr)
# # Test 1