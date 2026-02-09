import memory as mem
import state

async def update_sys_state(cache, key: str, outer_key: str, inner_key: str, val):
    sys_state = await mem.get_user_value(cache, key)
    print('sys_state : ', sys_state)
    sys_state = state.set_param(sys_state, outer_key, inner_key, val)
    await mem.set_user_value(cache, key, sys_state)
    print("updated sys_state: ", sys_state)
    return sys_state

def cdi_to_state(sys_state, cdi_arr):
    if len(cdi_arr) >= 18:
        sys_state['art_ph']['val'] =  cdi_arr[1]
        sys_state['art_pco2']['val'] = cdi_arr[2]
        sys_state['art_po2']['val'] = cdi_arr[3]
        sys_state['art_temp']['val'] = cdi_arr[4]
        sys_state['hco3']['val'] = cdi_arr[5]
        sys_state['base']['val'] = cdi_arr[6]
        sys_state['cso2']['val'] = cdi_arr[7]
        sys_state['k']['val'] = cdi_arr[8]
        sys_state['vo2']['val'] = cdi_arr[9]
        sys_state['do2']['val'] = cdi_arr[10]
        sys_state['ven_ph']['val'] = cdi_arr[12]
        sys_state['ven_pco2']['val'] = cdi_arr[13]
        sys_state['ven_po2']['val'] = cdi_arr[14]
        sys_state['ven_temp']['val'] = cdi_arr[14]
        sys_state['so2']['val'] = cdi_arr[15]
        sys_state['hct']['val'] = cdi_arr[16]
        sys_state['hb']['val'] = cdi_arr[17]
    return sys_state