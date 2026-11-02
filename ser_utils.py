import onque as oq

# "<gbm>m:state|" + set_fio2 + "|" + set_total_flow + "|" + set_oxygen_flow + "|" + set_air_flow + "|" + fio2 + "|" + oxygen_flow + "|" + air_flow;

def process_cdi_msg(msg):
    i = 0
    cdi_arr = []
    while msg[i] != '\n':
        
        print(msg[i])
        if(msg[i] == '\t'):
            numb_var = None
            sign = 1
            dec = 1
            i += 1

            while not (msg[i] == '\t' or msg[i] == '\n'):
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
                print(f'msg[i] : {msg[i]}, numb_var : {numb_var}')

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
            
def parse_ser_msg(device:str, msg: str, ux_q):
    if msg:
        if isinstance(msg, bytes):
            msg.decode("utf-8")
        if device == 'cdi':
            serial_data = process_cdi_msg(msg)
        elif device == 'gbm':
            serial_data = process_gbm(msg)

        oq.feed_q(ux_q, 'ser_data', device, serial_data)


    

if __name__ == '__main__':
    test =b' 09:41:33\t7.14\t ---\t ---\t-26.4\t --\t --\t ---\t -.-\t ---\t -.-\t    \t7.26\t ---\t ---\t25.5\t ---\t 25%\t  \r\n'
    test = test.decode('utf-8')
    print(test)
    # test = bytearray(test, "utf-8")
    arr = build_cdi_arr(test)
    print("CDI Arr: ", arr)
    test = b' 18:25:09\t6.54\t 040\t ---\t30.4\t 03 \t -- \t ---\t'
    l = len(test)
    print(f'length: {l}')
    i = 0
    for i in range(l):
        print(f'len : {i} and {test[i]} and {chr(test[i])}')

# Test 1