import asyncio
import db
import onque as oq

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
    def __init__(self):
        self.que = asyncio.Queue()

    async def put_db_item(self, cm_type, anex=None, case_id=None, data=None):
        await self.que.put(que_item(cm_type, anex, case_id, data))
    
    async def get_db_item(self):
        return await self.que.get()

async def archive_task(archive_que: db_que, db_obj, cc):
    while True:
        q_item = archive_que.get_db_item()
        parse_archive_que(q_item, db_obj, cc)

def parse_archive_que(q_item: que_item, db_obj, cc=None):
    db_type = q_item.get_cm_type()
    db_anex = q_item.get_anex()
    db_data = q_item.get_data()
    db_case_id = q_item.get_case_id()
    print(f'parse_archive_que -> db_que_item {db_type, db_anex, db_case_id, db_data}')

    if db_type == 'cn_list':
        brod_item = db.inspect_table(db_obj.engine, db_obj.metadata.tables['cases'], param_list=['case_id'])

    elif db_type == 'full_case' and isinstance(db_anex, int) and db_anex == 0:
        cs_data = db.get_case_data(db_obj.engine, db_obj.metadata, db_anex)
        xlsx_file_name = 'case_data'
        db.build_xlsx_file(cs_data, 'case_data')


    elif db_type == 'get_data':

        if db_anex == 'notes':
            brod_item = db.inspect_table(db_obj.engine, db_obj.metadata.tables['notes'], db_case_id)
        elif db_anex == 'cdi':
            brod_item = db.inspect_table(db_obj.engine, db_obj.metadata.tables['cdi_data'], db_case_id )

    elif db_type == 'param_list':
        brod_item = db.get_all_param(db_obj.engine, db_obj.metadata)

    elif db_type == 'entry':
        if db_anex == 'note':
            db.note_entry(db_obj.engine, db_case_id, db_data)
        elif db_anex == 'cdi':
            db.cdi_entry(db_obj.engine, db_case_id, db_data)
        elif db_anex == 'new_case':
            db.create_case(db_obj.engine, '', db_case_id)

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

async def test_parse_archive_que(test_que: db_que, db_obj):
    await test_que.put_db_item('cn_list')
    await test_que.put_db_item('full_case')
    await test_que.put_db_item('cn_list')

    q_item = await test_que.get_db_item()
    result = parse_archive_que(q_item, db_obj)
    print(f'parse_archive_que -> {result}')
    

### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### ### UNIT TEST ### 

async def main():
    db_parth = 'sqlite:///data_vault.db'
    db_obj = db.Db_Obj(db_parth)
    test_que = db_que()
    test = que_item('test_type', 'test_command', 1, 'test_data')
    await test_que.put_db_item('cm_type', 'anex', 1, 'data')
    test_item = await test_que.get_db_item()


    test_que_item_response()
    await test_parse_archive_que(test_que, db_obj)

if __name__ == "__main__":
    asyncio.run(main())