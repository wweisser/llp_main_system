import asyncio
import db
import onque as oq
import time
import random

class Que_Item:
    def __init__(self, cm_type:str, case_id:int=None, anex:str=None, data=None, begin:str=None, to:str=None, n:int=None):
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
        await self.que.put(Que_Item(cm_type, case_id, anex, data, begin, to, n))
    
    async def get_db_item(self):
        return await self.que.get()

async def parse_archive_que(q_item: Que_Item, db_obj: db.Db_Obj, cc=None):
    type = q_item.get_cm_type()
    data = q_item.get_data()
    anex = q_item.get_anex()
    case_id = q_item.get_case_id()
    begin = q_item.get_begin()
    to = q_item.get_to()
    n = q_item.get_n()
     
    if type == 'cil': #case id list
        cn_list = db.inspect_table(db_obj, 'cases', param_list=['case_id'])
        await oq.broadcast_item('cn', 'cn_list', cn_list['case_id'], cc)

    elif type == 'stu' and isinstance(data, int):
        conf = db.update_start_time(db_obj, case_id=case_id, new_start_time=data)
        if conf:
            await oq.broadcast_item('st', 'st_update', data, cc)
            print(f'parse_archive_que -> new start time {data}\n')

    elif type == 'tlc':
        df = db.build_download_file(db_obj, case_id)
        if df:
            await oq.broadcast_item('cd', 'total_case', 'excel file was created', cc)

    elif type == 'ext' and isinstance(case_id, int) and case_id != 0:
        print(f'parse_archive_que -> get extraction note command registered\n')
        extct = None
        if (anex == 'notes' or anex == 'cdi_data' or 'cases') and (not data or isinstance(data, list)):
            extct = db.inspect_table(db_obj, table=anex, case_id=case_id, param_list=data, begin=begin, to=to, n=n)
        if extct:
            await oq.broadcast_item('ext', data, extct, cc)
            print(f'parse_archive_que -> note brod item: {extct}\n')

    elif type == 'entry':
        if anex == 'note':
            db.note_entry(db_obj, case_id, data)
        elif anex == 'cdi':
            db.cdi_entry(db_obj, case_id, data)
        elif anex == 'new_case':
            db.create_case(db_obj, data, case_id)


async def start_archive_task(db_obj:db.Db_Obj, db_que: Db_Que, cc:list):
    while(True):
        qi = await db_que.get_db_item()
        if qi:
            parse_archive_que(q_item=qi, db_obj=db_obj, cc=cc)


### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### 

def test_que_item_response():
    t_type = 'test_type'
    t_anex = 'anex'
    t_case_id = 1
    t_data = 'test_data'
    t_begin = 'begin'
    t_to = 'to'
    t_n = 500

    test_item = Que_Item(t_type, t_case_id, t_anex, t_data, t_begin, t_to, t_n)
    assert test_item.get_cm_type() == t_type
    assert test_item.get_anex() == t_anex
    assert test_item.get_case_id() == t_case_id
    assert test_item.get_data() == t_data
    assert test_item.begin == t_begin
    assert test_item.to == t_to
    assert test_item.n == t_n
    assert type(test_item.get_time()) == int
    print(f'test_que_item_response -> unit tests cleared')

async def tst(que: Db_Que, cm_type: str, cc, anex=None, case_id=None, data=None, ):
    await que.put_db_item(cm_type, anex, case_id, data)
    q_item = await que.get_db_item()
    await parse_archive_que(q_item, que.db_obj, cc)
    # print(f'tst -> que item {}')
    if not cm_type == 'entry':
        result = await cc['tq'].get()
        return result

async def test_parse_archive_que(que: Db_Que, db_obj, cc):
    # t_cn_list = await tst(que, 'cil', cc)
    # print(f'test_parse_archive_que -> t_cn_list: {t_cn_list}')
    # assert isinstance(t_cn_list, dict)
    t_full_case = await tst(que, 'tlc', cc)
    print(f'test_parse_archive_que -> t_full_case: {t_full_case}')
    assert isinstance(t_full_case, dict)
    # param_list = await tst(que, 'stu', cc, case_id=89, anex='', data=45835643 )

    # param_list = await tst(que, 'ext', cc, case_id=89, anex='cases')
    # print(f'test_parse_archive_que -> param_list: {param_list}')
    # assert isinstance(param_list, dict)
  

    # cdi_arr = []
    # for i in range(16):
    #     cdi_arr.append(round(random.randint(1, 100)/random.randint(1, 100), 2))
    # await tst(que, 'entry', cc, anex='note', case_id=1, data=f'test note nr: {random.randint(1, 100)}')
    # print(f'test_parse_archive_que -> note entry was send')
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

    asyncio.create_task(start_archive_task(db_obj=db_obj, db_que=test_que, cc=test_cc))
    # await test_parse_archive_que(test_que, db_obj, test_cc)

if __name__ == "__main__":
    asyncio.run(main())