
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

def ser_run(con_arr: list):
    """
    1: analyses if there are new serial ports, that are not in the list if yes,
    creates a list item and listens for message
    2: If there is no device attached to the port, 
    it takes the message and selects a device and attaches it gives the list item a device
    """
    return None



