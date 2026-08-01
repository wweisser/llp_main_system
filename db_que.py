import asyncio
import db
import onque as oq

class que_item:
    def __init__(self, cm_type, anex, case_id, data):
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

    def get_cm_time(self):
        return self.time


class db_que:
    def __init__(self):
        self.que = asyncio.Queue()

    async def put_db_item(self, cm_type, command, data):
        await self.que.put(que_item(cm_type, command, data))
    
    async def get_db_item(self):
        return await self.que.get()

async def archive_access(archive_que: db_que, db_obj, cc):
    while True:
        db_que_item = archive_que.get_db_item()
        if isinstance(db_que_item, que_item):
            db_type = db_que_item.get_cm_type()
            db_anex = db_que_item.get_anex()
            db_data = db_que_item.get_data()
            db_case_id = db_que_item.get_case_id()
            if db_type == 'cn_list':
                cn_list = db.inspect_engine(db_obj.metadata, 'cases')
                # oq.broadcast_item('case_id', 'cn_list', cn_list)
            elif db_type == 'full_case' and isinstance(db_anex, int) and db_anex == 0:
                cs_data = db.get_case_data(db_obj.engine, db_obj.metadata, db_anex)
                xlsx_file_name = 'case_data'
                db.build_xlsx_file(cs_data, 'case_data')
                oq.broadcast_item('download', 'case_data', xlsx_file_name, cc)
            elif db_type == 'param':
                pass
            elif db_type == 'param_list':
                db.get_all_param(db_obj.engine, db_obj.metadata)
            elif db_type == 'entry':
                if db_anex == 'note':
                    db.note_entry(db_obj.engine, db_case_id, db_data)
                elif db_anex == 'cdi':
                    db.cdi_entry(db_obj.engine, db_case_id, db_data)
                elif db_anex == 'new_case':
                    db.create_case(db_obj.engine, '', db_case_id)


async def start_archive():
    archive_que = db_que

if __name__ == "__main__":
    db_parth = 'sqlite:///data_vault.db'
    db_obj = db.Db_Obj(db_parth)
    test_que = db_que()
    test = que_item('test_type', 'test_command', 1, 'test_data')
    test_que.put_db_item('cm_type', 'command', 'data')
    test_item = test_que.get_db_item()
    print(test_item.get_cm_type())
    print(test_item.get_command())
    print(test_item.get_data())