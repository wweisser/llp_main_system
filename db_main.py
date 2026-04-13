import db_utils as du
import memory
import onque as oq
import asyncio
from datetime import datetime

async def db_to_gui(gui_q, parth: str, val: str, range: int, case_number: int):

    async def execute(gui_q, parth: str, val: str, range: int, case_number: int):
        val_arr = du.get_val(parth, val, range, case_number)
        q_item = oq.create_q_item('db', 'val_arr', val_arr)
        await oq.feed_queue(gui_q, q_item)

    return await asyncio.to_thread(execute(gui_q, parth, val, range, case_number))

async def start_case_record(sys_state, ux_q, cache, key):
    archive_item = sys_state
    counter = 0
    if archive_item['system']['case_number'] != 0:
        print('autosave online')
        while True:
            if archive_item['system']['autosave'] and archive_item['system']['case_number'] != 0:
                if counter > 30:
                    sys_state = memory.get_state_from_cache(cache, key)
                    record_item = oq.create_q_item('archive', 'entry', sys_state)
                    await oq.feed_queue(ux_q, record_item)
                    print('entry request was send')
                    sys_state['note'] = ''
                    memory.put_state_to_cache(cache, key, sys_state)
                    counter = 0
            else:
                print('autosave was canceled')
                break
            counter += 1
            await asyncio.sleep(1)
    else:
        return None


#if __name__ == '__main__':
