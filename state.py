import json

def get_json(dat):
    if isinstance(dat, str):
        try:
            data = json.loads(dat)
            return data
        except:
            if isinstance(dat, dict):
                return dat
    return None

def get_sys_val(sys_json, param: str, val: str):
    if isinstance(sys_json, dict):
        return sys_json[param][val]
    elif isinstance(sys_json, str):
        data = get_json(sys_json)
        if data:
            return data[param][val]
        else:
            print("ERROR wrong datatype")
            return None
    else:
        print("ERROR wrong datatype")
        return None

def update_sys_json(sys_json: str, param: str, val: str, new_val: str):
    data = json.loads(sys_json)
    data[param][val] = new_val
    sys_json =  json.dumps(data)
    return sys_json

def pack_json(file: dict):
    try:
        msg = json.dumps(file)
        return msg
    except Exception as e:
        print("output could not be processed")
        raise   

def create_state():
    sys_state = {
        "case_id": 0,
        "autosave": False,
        "start_time": 0,
        "start_time_hope": 0,
        "start_time_cor": 0,
        "start_time_nmp": 0,
        "perfusion_time": 0,
        "clock_time": 0,
        "perfusion_mode": "",

        "gbm_align": False,
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
    return sys_state

if __name__ == "__main__":
    state_json = create_state()
    print(type(state_json))
    state_json = pack_json(state_json)
    data = get_sys_val(state_json, 'k', 'val')
    print(data)
    state_json = update_sys_json(state_json, 'k', 'val', '4.5')
    data = get_sys_val(state_json, 'k', 'val')
    print(data)