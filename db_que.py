import asyncio
import db
import onque as oq
import time
import random

class que_item:
    def __init__(self, cm_type, case_id=None, anex=None, data=None, begin=None, to=None, n=None):
        now = int(time.time())
        self.type = cm_type
        self.case_id = case_id
        self.anex = anex
        self.data = data
        self.begin = begin
        self.to = to
        self.n = n
        self.time = now


    def get_data(self):
        return self.data
    
    def get_anex(self):
        return self.anex
    
    def get_cm_type(self):
        return self.type

    def get_case_id(self):
        return self.case_id

    def get_begin(self):
        return self.begin

    def get_to(self):
        return self.to

    def get_n(self):
        return self.n
    
    def get_time(self):
        return self.time

    def get_param(self):
        return self.type, self.case_id, self.anex, self.data, self.begin, self.to, self.n

class Db_Que:
    def __init__(self, db_obj):
        self.que = asyncio.Queue()
        self.db_obj = db_obj

    async def put_db_item(self, cm_type: str, anex=None, case_id=None, data=None, begin=None, to=None, n=None):
        await self.que.put(que_item(cm_type, case_id, anex, data, begin, to, n))
    
    async def get_db_item(self):
        return await self.que.get()

async def archive_task(archive_que: Db_Que, db_obj, cc):
    while True:
        q_item = archive_que.get_db_item()
        parse_archive_que(q_item, db_obj, cc)

async def parse_archive_que(q_item: que_item, db_obj: db.Db_Obj, cc=None):
    type = q_item.get_cm_type()
    data = q_item.get_data()
    anex = q_item.get_anex()
    case_id = q_item.get_case_id()
    begin = q_item.get_begin()
    to = q_item.get_to()
    n = q_item.get_n()
     
    if type == 'cnl':
        cn_list = db.inspect_table(db_obj.engine, db_obj.metadata.tables['cases'], param_list=['case_id'])
        await oq.broadcast_item('cn', 'cn_list', cn_list['case_id'], cc)

    elif type == 'tlc':
        df = db.build_download_file(db_obj, case_id)
        if df:
            await oq.broadcast_item('cd', 'total_case', 'excel file was created', cc)

    elif type == 'ext' and isinstance(case_id, int) and case_id != 0:
        print(f'parse_archive_que -> get extraction note command registered\n')
        extct = None
        if (anex == 'note' or anex == 'cdi_data') and (not data or isinstance(data, list)):
            print(f'db_type -> PING\n')
            extct = db.inspect_table(db_obj.engine, table=db_obj.metadata.tables[anex], case_id=case_id, param_list=data, begin=begin, to=to, n=n)
            print(f'parse_archive_que -> note brod item: {extct}\n')
        if extct:
            await oq.broadcast_item('ext', data, extct, cc)

    elif type == 'ent':
        if anex == 'note':
            db.note_entry(db_obj.engine, case_id, data)
        elif anex == 'cdi':
            db.cdi_entry(db_obj.engine, case_id, data)
        elif anex == 'new_case':
            db.create_case(db_obj.engine, data, case_id)


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
    if not cm_type == 'entry':
        result = await cc['tq'].get()
        return result

async def test_parse_archive_que(que: Db_Que, db_obj, cc):
    # t_cn_list = await tst(que, 'cnl', cc)
    # print(f'test_parse_archive_que -> t_cn_list: {t_cn_list}')
    # assert isinstance(t_cn_list, dict)
    t_full_case = await tst(que, 'tlc', cc)
    print(f'test_parse_archive_que -> t_full_case: {t_full_case}')
    assert isinstance(t_full_case, dict)
    # param_list = await tst(que, 'extraction', cc, case_id=1, anex='cdi_data', data=['ven_po2', 'glu', 'base'], )
    # print(f'test_parse_archive_que -> param_list: {param_list}')
    # assert isinstance(param_list, dict)

    cdi_arr = []
    for i in range(16):
        cdi_arr.append(round(random.randint(1, 100)/random.randint(1, 100), 2))
    # await tst(que, 'entry', cc, anex='cdi', case_id=1, data=cdi_arr)
    # print(f'test_parse_archive_que -> cdi entry was send')
    # await tst(que, 'entry', cc, anex='note', case_id=1, data=f'late test not {random.randint(1, 100)}')
    # print(f'test_parse_archive_que -> cdi entry was send')

### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### 

async def main():
    db_parth = 'sqlite:///data_vault.db'
    db_obj = db.Db_Obj(db_parth)
    test_que = Db_Que(db_obj)
    tq = asyncio.Queue()
    test_cc: dict[asyncio.Queue] = {}
    test_cc['tq'] = tq

    test_que_item_response()
    await test_parse_archive_que(test_que, db_obj, test_cc)

if __name__ == "__main__":
    asyncio.run(main())