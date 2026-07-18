from sqlalchemy import (
    create_engine, String, Integer, Float, ForeignKey, MetaData, Table, inspect, select
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import time
import pandas as pd

import random

class Base(DeclarativeBase):
    pass

class Cases(Base):
    __tablename__ = "cases"

    # id: Mapped[int]                 = mapped_column(Integer)
    comment: Mapped[str | None]     = mapped_column(String)
    case_id: Mapped[int]            = mapped_column(Integer, primary_key=True,  nullable=False,)
    start_time: Mapped[int | None]  = mapped_column(Integer, default=lambda: int(time.time()))
    
    # Readings can be use to get all values related to a case, e.g. for plotting or exporting
    case_to_cdi_link:   Mapped[list["CDI_Data"]] = relationship(back_populates="cases")
    case_to_note_link:  Mapped[list["Notes"]] = relationship(back_populates="cases")

    def get_table(self):
        return {'comment': self.comment, 
                'case_id': self.case_id, 
                'start_time': self.start_time}


class CDI_Data(Base):
    __tablename__ = "cdi_data"

    id:         Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    case_id:    Mapped[int] = mapped_column(ForeignKey("cases.case_id"), nullable=False)
    ts:         Mapped[int] = mapped_column(Integer, nullable=False)   # Unix-Zeit (oder ms)

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

    cases: Mapped["Cases"] = relationship(back_populates="case_to_cdi_link")

    def get_table(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'ts': self.ts,
            'device_id': self.device_id,
            'art_ph': self.art_ph, 
            'art_pco2': self.art_pco2, 
            'art_po2': self.art_po2, 
            'ven_ph': self.ven_ph, 
            'ven_pco2': self.ven_pco2, 
            'ven_po2': self.ven_po2, 
            'cso2': self.cso2, 
            'so2': self.so2, 
            'hb': self.hb, 
            'hct': self.hct, 
            'hco3': self.hco3, 
            'base': self.base, 
            'k': self.k
        }

class Notes(Base):
    __tablename__ = "notes"
    id:         Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    case_id:    Mapped[int] = mapped_column(ForeignKey("cases.case_id"), nullable=False)
    ts:         Mapped[int] = mapped_column(Integer, nullable=False)   # Unix-Zeit (oder ms)

    note:       Mapped[str] = mapped_column(String)

    cases: Mapped["Cases"] = relationship(back_populates="case_to_note_link")
    
    def get_table(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'ts': self.ts,
            'Notes': self.note
        }

def create_case(engine, comment, case_id):
    with Session(engine) as session:
        existing = session.scalars(select(Cases).where(Cases.case_id == case_id)).one_or_none()
        if not existing:
            case = Cases(
                comment =       comment,
                case_id =       case_id,
                start_time =    int(time.time())
            )
            session.add(case)
            session.commit()
        else:
            print(f'create_case -> case allready exists')

def cdi_entry(engine, case_id, cdi_arr):
    with Session(engine) as session:
        case = session.get(Cases, case_id)
        if case:
            cdi_data_entry_item = CDI_Data(
                case_id =   case_id,
                ts =        int(time.time()),

                art_ph     = cdi_arr[0],
                art_pco2   = cdi_arr[1],
                art_po2    = cdi_arr[2],
                ven_ph     = cdi_arr[3],
                ven_pco2   = cdi_arr[4], 
                ven_po2    = cdi_arr[5], 
                cso2       = cdi_arr[6], 
                so2        = cdi_arr[7],
                hb         = cdi_arr[8],
                hct        = cdi_arr[9],
                hco3       = cdi_arr[10],
                base       = cdi_arr[11],
                k          = cdi_arr[12],
            )
            case.case_to_cdi_link.append(cdi_data_entry_item)
        session.commit()

def note_entry(engine, case_id, new_note: str):
    with Session(engine) as session:
        case = session.get(Cases, case_id)
        if case:
            note_entry_item = Notes(
                case_id =   case_id,
                ts =        int(time.time()),
                note = new_note,
            )
            print(f'note_entry -> note : {new_note}')
        case.case_to_note_link.append(note_entry_item)
        session.commit()

def transpone(table_dict:dict):
    """Takes the dict with a list of values for each parameter.
    Returns da list of dicts. One dict for every row with parameter as identifier
    and the adjacend value."""
    table_tranposed = []
    length = len(table_dict['case_id'])
    print(f'transpone -> length: {length}')
    for i in range(length):
        row = {}
        for param in table_dict:
            print(f'transpone -> param: {param}')
            row[param] = table_dict[param][i]
        table_tranposed.append(row)
    return table_tranposed

def inspect_table(engine, table, param_list: list, case_id=None, begin=None, to=None):
    """returns a dictionary in which each item of the param_list acts as an identifier 
    to a list of values"""
    if table is not None:
        print(f'inspect_table -> type: {type(table)}')
        with Session(engine) as session:
            result_dict = {}
            for param in param_list:
                col_adress = (getattr(table.c, param)) #.c steht hier immer für columns und ist eine convention bei metadata
                sdi = select(col_adress)
                if case_id:
                    sdi = sdi.where(table.c.case_id == case_id)
                if begin:
                    sdi = sdi.where(table.c.ts > begin)
                if to:
                    sdi = sdi.where(table.c.ts < to)
                result = session.scalars(sdi).all()

                result_dict[param] = result
            print(f'inspect_table -> result dict{result_dict}\n')
            
            return result_dict
    else:
        print(f'inspect_table -> engine or table do not exist\n')

def inspect_engine(metadata):
    """Shows all tables in the engine"""
    # print(f'inspect_engine -> tables: {metadata.tables}')
    return metadata.tables.values()

def get_cols(table):
    column_names = list(table.columns.keys())
    return column_names

def get_case(engine, case_id):
    if engine and case_id:
        with Session(engine) as session:
            sdi = (select(Cases)
                   .join(CDI_Data.cases)
                   .join(Notes.cases)
                   .where(Cases.case_id == case_id)
                )
            result = session.scalars(sdi).all()
            print(f'get_case -> {result}')

# Functionality: Base is the basic register clas 
def case_loader(engine, metadata, case_id: int):
    """Gets db and case_id. Then calls inspect_table for each table in the engine.
    Then calls transpone for every result. Creates the a dict of dicts
    with table_name as identifier and the transponed table data as value."""
    tables = inspect_engine(metadata)
    print(f'case_loader -> tables : {tables}\n')
    case_data = {}
    for table in tables:
        print(f'case_loader -> table : {table} type : {type(table)}\n')
        params = get_cols(table)
        table_data = inspect_table(engine, table, params, case_id)
        case_data[table.name] = transpone(table_data)
        print(f'case_loader -> case_data : {case_data}\n')
        # trnsp_tbl = transpone(table_data)
    return case_data

def get_case_data(engine, metadata, case_id: int):
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

if __name__ == "__main__":
    engine = create_engine('sqlite:///data_vault.db')
    metadata = MetaData()
    metadata.reflect(bind=engine)
    Base.metadata.create_all(engine)
    tables = inspect_engine(metadata)

    create_case(engine, 'test case', 1)
    inspect_engine(metadata)

    # inspect_table(engine, CDI_Data, ['ts','art_ph', 'ven_ph'], 1)
    # inspect_table(engine, Notes, ['ts', 'note'], 1)
    # print(f'get_cols -> result : {get_cols(engine, metadata, CDI_Data)}')
    # table = Table("notes", metadata, autoload_with=engine)
    # case_data = case_loader(engine, metadata, 1)
    # case_data = inspect_table(engine, metadata.tables["notes"], ['ts', 'note'], 1)
    result = get_case_data(engine, metadata, 1)
    print(f'main -> notes tables: {result}')

    df = pd.DataFrame(result)
    df.to_excel("output.xlsx", sheet_name="Daten", index=False)

    # user_table = Table("cases", metadata, autoload_with=engine)
    # CDI_Data.__table__.drop(engine)
    # Base.metadata.drop_all(engine)

    # cdi_arr = []
    # for i in range(13):
    #     cdi_arr.append(round(random.randint(1, 100)/random.randint(1, 100), 2))
    # print(f'cdi_arr -> {cdi_arr}\n')
    # cdi_entry(engine, 1, cdi_arr)
    # note_entry(engine, 1, 'liver weight 2054')
    # get_case(engine, 1)
    # inspect_engine(engine)



