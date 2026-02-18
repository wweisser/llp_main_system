from diskcache import Cache
import os


test_list = [00, 1, 2, 3, 00, 1, 2, 3, 999, 7, 0, -1]

def list_sort(cn_list):
    inter_list = []
    for id in cn_list:
        if isinstance(id, int):
            is_in_list = False 
            for x in inter_list:
                if x == id:
                    is_in_list = True
            if not is_in_list:
                inter_list.append(id)
    drp_dwn_list = []
    for id in inter_list:
        drp_dwn_list.append(str(id))
    return drp_dwn_list

print(list_sort(test_list))