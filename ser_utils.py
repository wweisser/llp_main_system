def select_device(input):
    if len(input) >= 100:
        res = input[:7]
        # print('len input :', len(input) )
        if (res[3] == 58 and res[6] == 58):
            # print("CDI detcted")
            return 'cdi'
        elif res == 'con_hub':
            return 'hub'
        else:
            print(f"Unknown device detected")
            return None

def ser_send(tx_q):

    return None



