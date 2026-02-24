import db_utils as du
import memory
import onque as oq
import asyncio
from datetime import datetime

async def db_entry(parth: str, table: str,  sys_state: dict):
    print('Data entry')
    return await asyncio.to_thread(du.execute_entry(parth, table, sys_state))

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
        # sys_state['system']['start_time'] = datetime.now()
        # sys_state['system']['autosave'] = True
        print('autosave online')
        while True:
            if archive_item['system']['autosave'] and archive_item['system']['case_number'] != 0:
                if counter > 10:
                    archive_item = memory.get_state_from_cache(cache, key)
                    record_item = oq.create_q_item('archive', 'entry', archive_item)
                    await oq.feed_queue(ux_q, record_item)
                    print('entry request was send')
                    counter = 0
            else:
                print('autosave was canceled')
                break
            counter += 1
            await asyncio.sleep(1)
    else:
        return None


#if __name__ == '__main__':
