import asyncio
import ser
import state


#      0 1  2   3   4    5   6   7   8  9  10 11  12 13  14  15  16   17
#Time pH CO2 O2 Temp HCO3 BE cSO2 K+ VO2 Q BSA pH CO2 O2 Temp SO2 HCT HGB

def cdi_to_state(sys_state: dict, cdi_arr: list):
    if len(cdi_arr) == 18:
        sys_state['art_ph'] =  cdi_arr[0]
        sys_state['art_pco2'] = cdi_arr[1]
        sys_state['art_po2'] = cdi_arr[2]
        sys_state['art_temp'] = cdi_arr[3]
        sys_state['hco3'] = cdi_arr[4]
        sys_state['base'] = cdi_arr[5]
        sys_state['cso2'] = cdi_arr[6]
        sys_state['k'] = cdi_arr[7]
        sys_state['vo2'] = cdi_arr[8]
        sys_state['q'] = cdi_arr[9]
        sys_state['bsa'] = cdi_arr[10]
        sys_state['ven_ph'] = cdi_arr[11]
        sys_state['ven_pco2'] = cdi_arr[12]
        sys_state['ven_po2'] = cdi_arr[13]
        sys_state['ven_temp'] = cdi_arr[14]
        sys_state['so2'] = cdi_arr[15]
        sys_state['hct'] = cdi_arr[16]
        sys_state['hb'] = cdi_arr[17]
    return sys_state

#String bcst_str = "<gbm>m:state|"set_fio2"|"set_total_flow"|"set_oxygen_flow"|"set_air_flow"|"fio2"|"oxygen_flow"|"air_flow";";

def gbm_to_state(sys_state: dict, glm_arr: list):
    if len(glm_arr) == 8:
        if glm_arr[0] == 0:
            sys_state['gbm_state'] = 'before selftest'
        elif glm_arr[0] == 1:
            sys_state['gbm_state'] = 'selftest passed'
        elif glm_arr[0] == 11:
            sys_state['gbm_state'] = 'active flow'
        elif glm_arr[0] == 12:
            sys_state['gbm_state'] = 'error during selftest'
        elif glm_arr[0] == 22:
            sys_state['gbm_state'] = 'error during active flow'
            
        sys_state["set_fio2"] = glm_arr[1]
        sys_state["set_gas_flow"] = glm_arr[2]
        sys_state["set_oxygen_flow"] = glm_arr[3]
        sys_state["set_air_flow"] = glm_arr[4]
        sys_state["gas_flow"] = glm_arr[6] + glm_arr[7]
        sys_state["fio2"] = glm_arr[5]
        sys_state["oxygen_flow"] = glm_arr[6]
        sys_state["air_flow"] = glm_arr[7]
    return sys_state

async def align_gbm(com_q: asyncio.Queue, sys_state: list):
    com_str = ""
    if sys_state['gbm_align']:
        current_fio2 = sys_state['fio2']
        current_po2 = sys_state['po2']
        set_po2 = sys_state['set_po2']
        set_fio2 = sys_state['set_fio2']
        factor_fio2 = 0;

        current_flow = sys_state['gas_flow']
        current_pco2 = sys_state['pco2']
        set_pco2 = sys_state['set_pco2']
        set_flow = sys_state['set_flow']
        factor_flow = 0;

        if current_po2 > 0:
            factor_fio2 = (set_po2-current_po2)/(current_po2*3)
            print(round(factor_fio2, 4))

        if abs(factor_fio2) > 0.03:
            set_fio2 = ((factor_fio2) * current_fio2) + current_fio2
            print(f'align_gbm -> set fio2: {set_fio2}')

        if current_po2 > 0:
            factor_flow = (current_pco2-set_pco2)/(current_pco2*2)
            print(round(factor_flow, 4))

        if abs(factor_flow) > 0.04:
            set_flow = ((factor_flow) * current_flow) + current_flow
            print(f'align_gbm -> set_flow: {round(set_flow, 3)}')


async def tester():
    q = asyncio.Queue
    sys_state =     sys_state = {
        "case_id": 0,
        "autosave": False,
        "start_time": 0,
        "start_time_hope": 0,
        "start_time_cor": 0,
        "start_time_nmp": 0,
        "perfusion_time": 0,
        "clock_time": 0,
        "perfusion_mode": "",

        "gbm_align": True,
        "set_gas_flow": 0,
        "set_fio2": 0,
        "set_oxygen_flow": 0,
        "set_air_flow": 0,
        "gas_flow": 0,
        "fio2": 0,
        "air_flow": 0,
        "oxygen_flow": 0,
        "set_po2": 0,
        "set_pco2": 0,

        "circulation": {
            "set_flow_ha": 0,
            "set_flow_pv": 0,
            "set_pressure_ha": 0,
            "set_pressure_pv": 0,
            "set_hct": 0,
            "set_filter_flow": 0,
            "set_substitude_flow": 0,
        },
        "temperature":{
            "set_temp": 0,
            "inflow_temp": 0,
            "outflow_temp": 0
        },
        "lab":{
            "ast": 0,
            "alt": 0,
            "bilirubin": 0,
            "urea": 0,
            "ap": 0,
            "kod": 0,
            "albumin": 0,
            "factor_v": 0,
            "gamma": 0,
        },
        "po2": 0,
        "pco2": 0,
        "glucose": 0,
        "hb": 0,
        "ph": 0, 
        "pco2": 0, 
        "po2": 0, 
        "hco3": 0, 
        "base": 0, 
        "cso2": 0, 
        "na": 0, 
        "k": 0, 
        "ca": 0, 
        "cl": 0,
        "vo2": 0, 
        "q": 0, 
        "ven_ph": 0, 
        "ven_pco2": 0, 
        "ven_po2": 0, 
        "so2": 0, 
        "hct": 0, 
        "hb": 0, 
        "lactate": 0, 
        "glucose": 0,
    }
    await align_gbm(q, sys_state)

if __name__ == "__main__":
    asyncio.run(tester())