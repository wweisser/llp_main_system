import db_utils as du
import memory
import onque as oq
import asyncio
import state

async def db_entry(parth: str, table: str,  sys_state: dict):
    return await asyncio.to_thread(du.execute_entry(parth, table, sys_state))

async def db_to_gui(gui_q, parth: str, val: str, range: int, case_number: int):

    def execute(gui_q, parth: str, val: str, range: int, case_number: int):
        val_arr = du.get_val(parth, val, range, case_number)
        q_item = oq.create_q_item('db', 'val_arr', val_arr)
        oq.feed_queue(gui_q, q_item)

    return await asyncio.to_thread(execute(gui_q, parth, val, range, case_number))

async def start_case_record(cache, key, ux_q):
    archive_item = state.create_state()
    counter = 0
    if archive_item['autosave']and archive_item['case_number'] != None:
        print('autosave online')
    while True:
        counter += 1
        archive_item = await memory.get_state_from_cache(cache, key)
        if archive_item['system']['autosave'] and archive_item['system']['case_number'] != 0:
            if counter > 30:
                oq.create_q_item('archive_request', 'entry', archive_item)
                counter = 0
            # Hier ggf noch eine mittelwerfunktion dazwischenschalten
        else:
            print('autosave offline')
        await asyncio.sleep(1)



#if __name__ == '__main__':
