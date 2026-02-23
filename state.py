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

def create_state(db_path: str):
    sys_state = {
        "system":{
            "case_number": 0,
            "autosave": None,
            "db_path": db_path,
            "start_time": 0,
            "perfusion_time": 0,
            "clock_time": 0,
            "perfusion_mode": "",
        },
        "organ_type": "liver",
        "notes": "",
        "art_flow":{
            "active": True,
            "unit": "[ml/min]", 
            "val": 0, 
            "lower_limit": 0, 
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "art_pressure":{
            "active": True,
            "unit": "[mmHg]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "art_temp":{
            "active": True,
            "unit": "[°C]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ven_flow":{
            "active": True,
            "unit": "[ml/min]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ven_pressure":{
            "active": True,
            "unit": "[mmHg]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ven_temp":{
            "active": True,
            "unit": "[°C]", 
            "val": 0, 
            "lower_limit": 0, 
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "return_temp":{
            "active": True,
            "unit": "[°C]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "art_ph":{
            "active": True,
            "unit": "[]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "art_pco2":{
            "active": True,
            "unit": "[mmHg]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "art_po2":{
            "active": True,
            "unit": "[mmHg]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "hco3":{
            "active": True,
            "unit": "[mmol/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "base":{
            "active": True,
            "unit": "[]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "cso2":{
            "active": True,
            "unit": "[%]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "na":{
            "active": True,
            "unit": "[mmol/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "k":{
            "active": True,
            "unit": "[mmol/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ca":{
            "active": True,
            "unit": "[mmol/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "cl":{
            "active": True,
            "unit": "[mmol/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        },
        "vo2":{
            "active": True,
            "unit": "[ml/kg/min]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "do2":{
            "active": True,
            "unit": "[ml/kg/min]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ven_ph":{
            "active": True,
            "unit": "[]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ven_pco2":{
            "active": True,
            "unit": "[mmHg]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "ven_po2":{
            "active": True,
            "unit": "[mmHg]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "so2":{
            "active": True,
            "unit": "[%]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "hct":{
            "active": True,
            "unit": "[%]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "hb":{
            "active": True,
            "unit": "[g/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "lactate":{
            "active": True,
            "unit": "[mmol/l]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "glucose":{
            "active": True,
            "unit": "[mg/dl]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        },
        "bilirubin":{
            "active": True,
            "unit": "[mg/dl]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        },
        "system_volume": 0,
        "filter_flow":{
            "active": True,
            "unit": "[ml/h]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }, 
        "substitude_flow":{
            "active": True,
            "unit": "[ml/h]", 
            "val": 0, 
            "lower_limit": 0,
            "upper_limit": 0,
            "total_volume": 0
        }
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