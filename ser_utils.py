import asyncio

def select_device(i):
    if isinstance(i, bytes):
        i = i.decode('utf-8')
    if i and len(i) > 10:
        # print('len input :', len(input) )
        if (i[3] == 58 and i[6] == 58 and i[9] == 9):
            # print("CDI detcted")
            return 'cdi'
        elif i[:5] == '<gbm>':
            return 'gbm'
        else:
            print(f"Unknown device detected")
            return None
    return None


# "<gbm>m:state|" + set_fio2 + "|" + set_total_flow + "|" + set_oxygen_flow + "|" + set_air_flow + "|" + fio2 + "|" + oxygen_flow + "|" + air_flow;

def parse_gbm(input: str) -> list:
    arr = []
    l = len(input)
    i = 0
    while i < l:
        if input[i] == '|' and i < l:
            i += 1
            numb = 0
            while i < l and input[i].isdigit():
                numb = numb * 10 + int(input[i])
                i += 1
            arr.append(numb)
        else:
            i += 1
    return arr
            
async def send_ser_command(com_q: asyncio.Queue, device: str, command: str):
    com_item = {
        'device': device, 
        'com': command
    }
    await com_q.put(com_item)


if __name__ == '__main__':
    test = b' 18:25:09\t6.54\t 040\t ---\t30.4\t 03 \t -- \t ---\t'
    print(select_device(test))
    l = len(test)
    print(f'length: {l}')
    i = 0
    for i in range(l):
        print(f'len : {i} and {test[i]} and {chr(test[i])}')
