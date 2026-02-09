# import state as state
from diskcache import Cache
import state

def create_cache(key: str, sys_state: dict):
    path = sys_state['system']['db_parth']
    if path == None:
        cache = Cache(directory=None)
    else:
        cache = Cache(path)
    cache[key] = sys_state
    return cache

def get_state_from_cache(cache, key):
    try:
        return cache.get(key, retry=True)
    except:
        return None

# Takes a dict and puts it to the cache memory 
def put_state_to_cache(cache, key: str, state: dict):
    try:
        cache.set(key, state, retry=True)
        return 1
    except:
        return None

def update_val_cache(cache, key, sys_state: dict, data: str, parameter: str, val:str):
        sys_state = get_state_from_cache(cache, key)
        sys_state[parameter][val] = data
        put_state_to_cache(cache, key, sys_state)

def test():
    sys_state = state.create_state(None)
    # print(sys_state)
    cache = create_cache('key', sys_state)
    sys_state = get_state_from_cache(cache, 'key')
    print(sys_state['k']['val'])
    sys_state['k']['val'] = 2
    print(sys_state['k']['val'])
    put_state_to_cache(cache, 'key', sys_state)
    sys_state = get_state_from_cache(cache, 'key')
    print(sys_state['k']['val'])
    update_val_cache(cache, 'key', sys_state, 4, 'k', 'val')
    sys_state = get_state_from_cache(cache, 'key')
    print(sys_state['k']['val'])

if __name__ == "__main__":
    test()



