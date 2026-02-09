
def select_device(input):
    if len(input) >= 100:
        res = input[:9]
        # print('len input :', len(input) )
        if (res[3] == 58 and res[6] == 58):
            # print("CDI detcted")
            return 'cdi'
        else:
            print(f"Unknown device detected")
            return None


