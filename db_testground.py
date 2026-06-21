from sqlalchemy import (
    create_engine, String, Integer, Float, ForeignKey, MetaData, Table, inspect, select
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import time
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
    device_id:  Mapped[str] = mapped_column(String, nullable=False)


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
                device_id = 'cdi',

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

def inspect_table(engine, table, param_list: list, case_id=None, begin=None, to=None):
    """returns a dictionary in which each item of the param_list acts as an identifier 
    to a list of values"""
    if engine and table:
        with Session(engine) as session:
            result_dict = {}
            for param in param_list:
                col_adress = (getattr(table, param))
                print(f'inspect_table -> param : {param}\n')
                sdi = select(col_adress)
                if case_id:
                    sdi = sdi.where(table.case_id == case_id)
                if begin:
                    sdi = sdi.where(table.ts > begin)
                if to:
                    sdi = sdi.where(table.ts < to)
                result = session.scalars(sdi).all()
                result_dict[param] = result
            print(f'inspect_table -> result dictionary {result_dict}\n')
            return result_dict
    else:
        print(f'inspect_table -> engine or table do not exist\n')


def inspect_engine(engine):
    """Shows all tables in the engine"""
    inspector = inspect(engine)
    print(f'inspect_engine -> tables: {inspector.get_table_names()}')

def get_case(engine, case_id):
    if engine and case_id:
        with Session(engine) as session:
            sdi = (select(Cases)
                   .join(CDI_Data.cases)
                   .join(Notes.cases)
                   .where(Cases.case_id == case_id)
                )
            result = session.scalars(sdi).all()
            # result = {
            #     'cases': cases,
            #     'cdi_data': cdi_data,
            #     'notes': notes
            # }
            print(f'get_case -> {result}')

# Functionality: Base is the basic register clas 
    
if __name__ == "__main__":
    engine = create_engine('sqlite:///data_vault.db')
    metadata = MetaData()

    inspect_engine(engine)
    Base.metadata.create_all(engine)
    create_case(engine, 'test case', 3)

    inspect_table(engine, Cases, ['case_id','start_time',])

    # user_table = Table("cases", metadata, autoload_with=engine)
    # user_table.drop(engine)

    # cdi_arr = []
    # for i in range(13):
    #     cdi_arr.append(round(random.randint(1, 100)/random.randint(1, 100), 2))
    # print(f'cdi_arr -> {cdi_arr}\n')

    # cdi_entry(engine, 3, cdi_arr)
    get_case(engine, 1)
    inspect_engine(engine)



