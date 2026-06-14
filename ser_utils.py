def select_device(i):
    if i and len(i) > 10:
        # print('len input :', len(input) )
        if (i[3] == 58 and i[6] == 58 and i[9] == 9):
            # print("CDI detcted")
            return 'cdi'
        elif i == 'hub':
            return 'hub'
        else:
            print(f"Unknown device detected")
            return None
    return None

def ser_send(tx_q):

    return None


if __name__ == '__main__':
    test = b' 18:25:09\t6.54\t 040\t ---\t30.4\t 03 \t -- \t ---\t'
    print(select_device(test))
    l = len(test)
    print(f'length: {l}')
    i = 0
    for i in range(l):
        print(f'len : {i} and {test[i]} and {chr(test[i])}')
