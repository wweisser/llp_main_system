
def str_to_numb(str):
    str_len = 0
    dec_fac_a = 10
    dec_fac_b = 1
    sign = 1
    numb = 0

    str_len = len(str)
    if(ord(str[0]) == 45):
        sign = -1
    for i in range(str_len):		
        if(ord(str[i]) >= 48 and ord(str[i]) <= 57):
            numb = (dec_fac_a*numb) + dec_fac_b*(ord(str[i]) - 48)
        if(ord(str[i]) == 46 or dec_fac_b < 1):
            dec_fac_b = dec_fac_b * 0.1
            dec_fac_a = 1
        numb = numb * sign
    return numb

def count_var(str):
    count = 0
    str_len = len(str)
    for i in range(str_len):
        if(str[i] == '\t'):
            count = count + 1
    return count
        
def process_input(input):
    x = ""
    y = 0
    i = 0
    numb_var = count_var(input)
    arr = [float("nan")] * numb_var
    arr_len = len(input) - 1
    for i in range(arr_len):
        if(input[i] != '\t'):
            x = f"{x}{input[i]}"
        if(input[i] != '\t' and input[i+1] == '\t' and y < numb_var):
            arr[y] = str_to_numb(x)
            arr[y] = round(arr[y], 2)
            x = ""
            y = y + 1
    return arr

def build_cdi_arr(serial_read: str):
    cdi_data_arr = process_input(serial_read)
    return cdi_data_arr

if __name__ == '__main__':
    test =b' 09:41:33\t7.14\t---\t---\t26.4\t--\t--\t---\t-.-\t---\t-.-\t \t7.26\t---\t---\t25.5\t---\t25%\t  test'
    # test = test.encode()
    if type(test) == bytes:
        print("Byte array type")
    test = test.decode("utf-8")
    arr = build_cdi_arr(test)
    print("CDI Arr: ", arr)
#b' 17:48:43\t6.59\t 038\t ---\t37.5\t 04 \t -- \t ---\t -.-\t ---\t -.-\t    \t6.66\t 027\t ---\t36.9\t ---\t ---\t    \r\n'