import asyncio
import db
import onque as oq

import random

class que_item:
    def __init__(self, cm_type, anex=None, case_id=None, data=None):
        self.type = cm_type
        self.anex = anex
        self.data = data
        self.case_id = case_id
        self.time = 0

    def get_data(self):
        return self.data
    
    def get_anex(self):
        return self.anex
    
    def get_cm_type(self):
        return self.type

    def get_case_id(self):
        return self.case_id

    def get_time(self):
        return self.time


class db_que:
    def __init__(self, db_obj):
        self.que = asyncio.Queue()
        self.db_obj = db_obj

    async def put_db_item(self, cm_type: str, anex=None, case_id=None, data=None):
        await self.que.put(que_item(cm_type, anex, case_id, data))
    
    async def get_db_item(self):
        return await self.que.get()

async def archive_task(archive_que: db_que, db_obj, cc):
    while True:
        q_item = archive_que.get_db_item()
        parse_archive_que(q_item, db_obj, cc)

async def parse_archive_que(q_item: que_item, db_obj, cc=None):
    db_type = q_item.get_cm_type()
    db_anex = q_item.get_anex()
    db_case_id = q_item.get_case_id()
    db_data = q_item.get_data()
    brod_item = None
    print(f'parse_archive_que -> db_que_item {db_type, db_anex, db_case_id, db_data}')

    if db_type == 'cn_list':
        cn_list = db.inspect_table(db_obj.engine, db_obj.metadata.tables['cases'], param_list=['case_id'])
        for cn in
        await oq.broadcast_item('cn', 'cn_list', brod_item, cc)
    elif db_type == 'full_case':
        cs_data = db.get_case_data(db_obj.engine, db_obj.metadata, db_anex)
        xlsx_file_name = 'case_data'
        brod_item = db.build_xlsx_file('xlsx_file_name', 'sheet1', cs_data, )
        if brod_item:
            await oq.broadcast_item('cd', 'full_case', 'excel file was created', cc)


    elif db_type == 'get_data' and isinstance(db_case_id, int) and db_case_id != 0:

        print(f'parse_archive_que -> get data note command registered\n')
        if db_anex == 'notes':
            brod_item = db.inspect_table(db_obj.engine, db_obj.metadata.tables['notes'], db_case_id)
            print(f'parse_archive_que -> note brod item: {brod_item}\n')
            await oq.broadcast_item('cd', 'notes', brod_item, cc)

        elif db_anex == 'cdi':
            brod_item = db.inspect_table(db_obj.engine, db_obj.metadata.tables['cdi_data'], db_case_id )
            await oq.broadcast_item('cd', 'cdi', brod_item, cc)

    elif db_type == 'param_list':
        brod_item = db.get_all_param(db_obj.engine, db_obj.metadata)
        await oq.broadcast_item('cd', 'param', brod_item, cc)

    elif db_type == 'entry':
        if db_anex == 'note':
            await db.note_entry(db_obj.engine, db_case_id, db_data)
        elif db_anex == 'cdi':
            await db.cdi_entry(db_obj.engine, db_case_id, db_data)
        elif db_anex == 'new_case':
            await db.create_case(db_obj.engine, '', db_case_id)

    return brod_item

### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### 

def test_que_item_response():
    t_type = 'test_type'
    t_anex = 'anex'
    t_case_id = 1
    t_data = 'test_data'
    test_item = que_item(t_type, t_anex, t_case_id, t_data)
    assert test_item.get_cm_type() == t_type
    assert test_item.get_anex() == t_anex
    assert test_item.get_case_id() == t_case_id
    assert test_item.get_data() == t_data
    assert type(test_item.get_time()) == int
    print(f'test_que_item_response -> unit tests cleared')

async def tst(que, cm_type: str, cc, anex=None, case_id=None, data=None, ):
    await que.put_db_item(cm_type, anex, case_id, data)
    q_item = await que.get_db_item()
    await parse_archive_que(q_item, que.db_obj, cc)
    result = await cc['tq'].get()
    return result

async def test_parse_archive_que(que: db_que, db_obj, cc):
    t_cn_list = await tst(que, 'cn_list', cc)
    print(f'test_parse_archive_que -> t_cn_list: {t_cn_list}')
    assert isinstance(t_cn_list, dict)
    t_full_case = await tst(que, 'full_case', cc)
    print(f'test_parse_archive_que -> t_full_case: {t_full_case}')
    assert isinstance(t_full_case, bool)
    param_list =  await tst(que, 'param_list', cc)
    print(f'test_parse_archive_que -> param_list: {param_list}')
    assert isinstance(param_list, dict)

    t_get_data = await tst(que, 'get_data', cc)
    print(f'test_parse_archive_que -> t_get_data: {t_get_data}')
    assert t_get_data == None
    t_get_data_notes = await tst(que, 'get_data', cc, 'notes', 1)
    print(f'test_parse_archive_que -> t_get_data_notes: {t_get_data_notes}')
    assert isinstance(t_get_data_notes, dict)
    t_get_data_cdi = await tst(que, 'get_data', cc, 'cdi', 1)
    print(f'test_parse_archive_que -> t_get_data_cdi: {t_get_data_cdi}')
    assert isinstance(t_get_data_cdi, dict)

    cdi_arr = []
    for i in range(13):
        cdi_arr.append(round(random.randint(1, 100)/random.randint(1, 100), 2))
    t_get_data_cdi = await tst(que, 'entry', 'cdi', 1)
    print(f'test_parse_archive_que -> t_get_data_cdi: {t_get_data_cdi}')
    assert isinstance(t_get_data_cdi, dict)

### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### 

async def main():
    db_parth = 'sqlite:///data_vault.db'
    db_obj = db.Db_Obj(db_parth)
    test_que = db_que(db_obj)
    tq = asyncio.Queue()
    test_cc: dict[asyncio.Queue] = {}
    test_cc['tq'] = tq

    test_que_item_response()
    await test_parse_archive_que(test_que, db_obj, test_cc)

if __name__ == "__main__":
    asyncio.run(main())