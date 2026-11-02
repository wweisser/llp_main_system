import time

def count_var(str):
    count = 0
    str_len = len(str)
    for i in range(str_len):
        if(str[i] == '\t'):
            count = count + 1
    return count
        
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

def build_cdi_arr(msg: str):
    cdi_data_arr = process_cdi_msg(msg)
    return cdi_data_arr
            

if __name__ == '__main__':
    test =b' 09:41:33\t7.14\t ---\t ---\t-26.4\t --\t --\t ---\t -.-\t ---\t -.-\t    \t7.26\t ---\t ---\t25.5\t ---\t 25%\t  \r\n'
    test = test.decode('utf-8')
    print(test)
    # test = bytearray(test, "utf-8")
    arr = build_cdi_arr(test)
    print("CDI Arr: ", arr)
#b' 17:48:43\t6.59\t 038\t ---\t37.5\t 04 \t -- \t ---\t -.-\t ---\t -.-\t    \t6.66\t 027\t ---\t36.9\t ---\t ---\t    \r\n'