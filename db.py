from sqlalchemy import (
    create_engine, String, Integer, Float, ForeignKey, MetaData, update, select
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import time
import pandas as pd

import random

class Base(DeclarativeBase):
    pass

class Db_Obj:

    def __init__(self, db_parth):
        self.engine = create_engine(db_parth)
        self.metadata = MetaData()
        # Fills all the information ablout table and db structure in the metadata object
        self.metadata.reflect(bind=self.engine)

    def get_tables(self):
        return metadata.tables
    
    def get_columns(self):
        return metadata.tables.column()

    def get_table_names(self):
        return metadata.tables.keys()
    
class Cases(Base):
    __tablename__ = "cases"

    # id: Mapped[int]                 = mapped_column(Integer)
    comment: Mapped[str | None]     = mapped_column(String)
    case_id: Mapped[int]            = mapped_column(Integer, primary_key=True,  nullable=False,)
    start_time: Mapped[int | None]  = mapped_column(Integer)
    
    # Readings can be use to get all values related to a case, e.g. for plotting or exporting
    case_to_cdi_link:   Mapped[list["CDI_Data"]] = relationship(back_populates="cases")
    case_to_note_link:  Mapped[list["Notes"]] = relationship(back_populates="cases")

    def get_table(self):
        return {'comment': self.comment, 
                'case_id': self.case_id, 
                'start_time': self.start_time}
    
    def get_st(self):
        return self.start_time

class CDI_Data(Base):
    __tablename__ = "cdi_data"

    id:         Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    case_id:    Mapped[int] = mapped_column(ForeignKey("cases.case_id"), nullable=False)
    ts:         Mapped[int] = mapped_column(Integer, nullable=False)   # Unix-Zeit (oder ms)
    p_ts:       Mapped[int] = mapped_column(Integer, nullable=False)  

    art_ph:     Mapped[float | None] = mapped_column(Float)
    art_pco2:   Mapped[float | None] = mapped_column(Float)
    art_po2:    Mapped[float | None] = mapped_column(Float)
    ven_ph:     Mapped[float | None] = mapped_column(Float)
    ven_pco2:   Mapped[float | None] = mapped_column(Float) 
    ven_po2:    Mapped[float | None] = mapped_column(Float) 
    cso2:       Mapped[float | None] = mapped_column(Float) 
    so2:        Mapped[float | None] = mapped_column(Float)
    hb:         Mapped[float | None] = mapped_column(Float)
    hct:        Mapped[float | None] = mapped_column(Float)
    hco3:       Mapped[float | None] = mapped_column(Float)
    base:       Mapped[float | None] = mapped_column(Float)
    k:          Mapped[float | None] = mapped_column(Float)
    glu:        Mapped[float | None] = mapped_column(Float)
    lac:        Mapped[float | None] = mapped_column(Float)
    vo2:        Mapped[float | None] = mapped_column(Float)


    cases: Mapped["Cases"] = relationship(back_populates="case_to_cdi_link")

class Notes(Base):
    __tablename__ = "notes"
    id:         Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    case_id:    Mapped[int] = mapped_column(ForeignKey("cases.case_id"), nullable=False)
    ts:         Mapped[int] = mapped_column(Integer, nullable=False)   # Unix-Zeit (oder ms)
    p_ts:       Mapped[int] = mapped_column(Integer, nullable=False)  

    note:       Mapped[str] = mapped_column(String)

    cases: Mapped["Cases"] = relationship(back_populates="case_to_note_link")

def create_case(engine, comment, case_id):
    with Session(engine) as session:
        existing = session.scalars(select(Cases).where(Cases.case_id == case_id)).one_or_none()
        if not existing:
            case = Cases(
                comment =       comment,
                case_id =       case_id,
                start_time =    0
            )
            session.add(case)
            session.commit()
            print(f'create_case -> New case with case_id {case_id} was created')
        else:
            print(f'create_case -> case allready exists')

def update_start_time(db: Db_Obj, case_id: int, new_start_time: int):
    tabelle = db.metadata.tables['cases']
    stmt = (
        update(tabelle)
        .where(tabelle.c.case_id == case_id)               # .c steht für die Spalten (Columns)
        .values(start_time=new_start_time)
    )
    with Session(engine) as session:
        session.execute(stmt)
        session.commit()

def cdi_entry(engine, case_id: int, cdi_arr: list):
    with Session(engine) as session:
        case = session.get(Cases, case_id)
        if case:
            start_time = case.get_st()
            time_stamp = int(time.time())
            cdi_data_entry_item = CDI_Data(
                case_id     = case_id,
                ts          = time_stamp,
                p_ts        = time_stamp - start_time,

                art_ph      = cdi_arr[0],
                art_pco2    = cdi_arr[1],
                art_po2     = cdi_arr[2],
                ven_ph      = cdi_arr[3],
                ven_pco2    = cdi_arr[4], 
                ven_po2     = cdi_arr[5], 
                cso2        = cdi_arr[6], 
                so2         = cdi_arr[7],
                hb          = cdi_arr[8],
                hct         = cdi_arr[9],
                hco3        = cdi_arr[10],
                base        = cdi_arr[11],
                k           = cdi_arr[12],
                glu         = cdi_arr[13],
                lac         = cdi_arr[14],
                vo2         = cdi_arr[15]
            )
            case.case_to_cdi_link.append(cdi_data_entry_item)
            session.commit()
            print(f'cdi_entry -> item : {cdi_data_entry_item}')



def note_entry(db, case_id: int, new_note: str):
    with Session(db.engine) as session:
        case = session.get(Cases, case_id)
        if case:
            start_time = case.get_st()
            time_stamp = int(time.time())
            note_entry_item = Notes(
                case_id =   case_id,
                ts         = time_stamp,
                p_ts       = time_stamp - start_time,

                note = new_note,
            )
            case.case_to_note_link.append(note_entry_item)
            print(f'note_entry -> item : {note_entry_item}')
        session.commit()
        return True
    return False

def transpone(table_dict:dict):
    """Takes the dict with a list of values for each parameter.
    Returns da list of dicts. One dict for every row with parameter as identifier
    and the adjacend value."""
    table_tranposed = []
    # print(f'transpone -> table_dict: {table_dict}\n')
    if 'case_id' in table_dict:
        length = len(table_dict['case_id'])
        for i in range(length):
            row = {}
            for param in table_dict:
                row[param] = table_dict[param][i]
            table_tranposed.append(row)
        # print(f'transpone -> table_tranposed: {table_tranposed}')
        return table_tranposed
    else:
        return None

# def build_result_dict(table, rows: list, param_list=None):
#     result_dict = {}
#     if param_list == None:
#         param_list = table.columns.keys()
#         # print(f'build_result_dict -> param_list: {param_list}\n')
#     # print(f'build_result_dict -> cols: {param_list}\n')
#     for param in param_list:
#         result_dict[param] = []
#     # print(f'build_result_dict -> result_dict: {result_dict}\n')
    
#     for row in rows:
#         i = 0;
#         for list in result_dict:
#             # print(f'build_result_dict -> param: {result_dict[list]}\n')
#             result_dict[list].append(row[i])
#             i += 1
#     # print(f'build_result_dict -> result_dict: {result_dict}\n')
#     return result_dict
 
def inspect_table(engine, table, case_id=None, param_list=None, begin=None, to=None, n=None):
    """returns a dictionary in which each item of the param_list acts as an identifier 
    to a list of values. param_list is not given, all parameters of the table are added to the return dict"""
    if engine == None or table == None:
        print(f'inspect_table -> table does not exist')
        return None
    table_params = list(table.columns.keys())
    sdi = []
    data = {}
    if not param_list:
        param_list = table_params
    for p in param_list:
        if p in table_params:
            sdi.append(getattr(table.c, p))
            data[p] = []
    sdi = select(*(sdi))
    if case_id != None:
        sdi = sdi.where(table.c.case_id == case_id)
    if begin:
        sdi = sdi.where(table.c.ts > begin)
    if to:
        sdi = sdi.where(table.c.ts < to)
    if n:
        sdi = sdi.order_by(table.c.ts.desc()).limit(n)
    if table.name == 'cases':
        sdi.order_by(table.c.case_id)
    else:
        sdi = sdi.order_by(table.c.ts)

    with Session(engine) as session:
        rows = session.execute(sdi).all()

    print(f'inspect_table -> rows: {rows} \n')

    for row in rows:
        i = 0
        for p in data:
            # print(f'inspect_table -> p: {p} \n')
            data[p].append(row[i])
            i += 1

    return data


# def case_loader(engine, metadata, case_id: int):
#     """Gets db and case_id. Then calls inspect_table for each table in the engine.
#     Then calls transpone for every result. Creates the a dict of dicts
#     with table_name as identifier and the transponed table data as value."""
#     tables = db.get_table_names()
#     print(f'case_loader -> tables : {tables}\n')
#     case_data = {}
#     for table in tables:
#         params = metadata.tables[table].column()
#         table_data = inspect_table(engine, table, case_id, params)
#         case_data[table.name] = transpone(table_data)
#         print(f'case_loader -> case_data : {case_data}\n')
#         trnsp_tbl = transpone(table_data)
#     return case_data

# def get_case_data(engine, metadata, case_id: int):
    """gets case_data form case_loader. Takes the cdi_data table as template_table.
    Then for each row in template table, every row in all other tables is searched for 
    a row with a ts val < the one in the template_table. The found row is then added to 
    Main table row and poped from the old table. The completed template_table is the returned"""
    case_data = case_loader(engine, metadata, case_id)
    if 'cdi_data' in case_data:
        template_table = case_data['cdi_data']
        case_data.pop('cdi_data', None)
        case_data.pop('cases', None)
        main_table = []

        print(f'get_case_data -> case_data: {case_data}')
        for row in template_table:
            row_mt = row
            for id in case_data:
                table = case_data[id]
                len_table = len(table)-1
                print(f'sort_case_data -> len_table: {len_table}')
                for i in range(len_table):
                    if table[i]['ts'] <= row['ts']:
                        table[i].pop('id', None)
                        table[i].pop('case_id', None)
                        table[i].pop('ts', None)
                        
                        row_mt = row | table[i]
                        table.pop(i)
            main_table.append(row_mt)
        print(f'sort_case_data -> main_table: {main_table}')
        return main_table
    else:
        return None

def build_xlsx_file(file_name: str, sheet_name: str, data: dict):
    try:
        file_name = file_name + '.xlsx'
        df = pd.DataFrame(data)
        df.to_excel(file_name, sheet_name=sheet_name, index=False)
        print(f'build_xlsx_file -> xlsx file was created')
        return True
    except:
        print(f'build_xlsx_file -> error case file was not created')
        return False

def build_download_file(db: Db_Obj, case_id: int):
    rd = inspect_table(db.engine, db.metadata.tables['cdi_data'], case_id)
    cdi_list = transpone(rd)
    rd = inspect_table(db.engine, db.metadata.tables['notes'], case_id)
    note_list = transpone(rd)

    rl = []
    for note in note_list:
        if note['ts'] < cdi_list[0]['ts']:
            rl.append(note)
            note_list.remove(note)

    for i in range(len(cdi_list) - 1):  
        for note in note_list:
            if cdi_list[i]['ts'] < note['ts'] and cdi_list[i+1]['ts'] >= note['ts'] :
                cdi_list[i]['note'] = note['note']
                note_list.remove(note)
        rl.append(cdi_list[i])
    for note in note_list:
        rl.append(note)
    print(f'rd_t_II: {rl}')

    return build_xlsx_file('test_file', 'sheet1', rl)



if __name__ == "__main__":
    db_parth = 'sqlite:///data_vault.db'
    engine = create_engine('sqlite:///data_vault.db')
    metadata = MetaData()
    metadata.reflect(bind=engine)
    Base.metadata.create_all(engine)
    db = Db_Obj(db_parth)

    create_case(db.engine, 'test case II', 2)
    print(inspect_table(engine, metadata.tables['cases'], param_list=['case_id', 'start_time']))
    update_start_time(db, 1, int(time.time()))

    print(inspect_table(engine, metadata.tables['cases'], param_list=['case_id', 'start_time']))
    # build_download_file(1)

    # note_entry(db, 1,  f'test_note {random.randint(1, 100)}')
    # print(f'\ncn_list -> result: {result}')

    # user_table = Table("cases", metadata, autoload_with=engine)

    # while True:
    #     cdi_arr = []
    #     for i in range(16):
    #         cdi_arr.append(round(random.randint(1, 100)/random.randint(1, 100), 2))
    #     print(f'cdi_arr -> {cdi_arr}\n')
    #     cdi_entry(engine, 1, cdi_arr)
    #     if random.randint(1, 4) == 1:
    #         note_entry(db, 1, f'test_note {random.randint(1, 100)}')
    #     time.sleep(6)
    # get_case(engine, 1)
    # inspect_engine(engine)

    # result = get_case_data(db.engine, db.metadata, 1)

    # table_data = inspect_table(db.engine, db.metadata.tables['cdi_data'])
    # print(f'\inspected_table -> {table_data}\n')

    # rd = inspect_table(db.engine, db.metadata.tables['notes'], 1)
    # rd_t_I = transpone(rd)
    # rd = inspect_table(db.engine, db.metadata.tables['cdi_data'], 1)
    # rd_t_II = transpone(rd)

    # print(f' rd_t_I: {rd_t_I}\n')

    # x = len(rd_t_II)-1
    # for i in range(x-1):
    #     y = len(rd_t_I)-1   
    #     for u in range(y):
    #         if rd_t_II[i]['ts'] <= rd_t_I[u]['ts'] and rd_t_II[i+1]['ts'] < rd_t_I[u]['ts'] :
    #             print(f'rd_t_II: {rd_t_II[i]}\n')

    #             rd_t_II[i]['notes'] = rd_t_I[u]['note']
    #             print(f' r: {rd_t_II[i]['notes']}\n')
    #             # rd_t_I.pop(u)
    # print(f'rd_t_II: {rd_t_II}')


    # build_xlsx_file('test_file', 'sheet1', rd_t_II)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#

    # CDI_Data.__table__.drop(engine)
    # Base.metadata.drop_all(engine)


