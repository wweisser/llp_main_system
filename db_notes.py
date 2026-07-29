from sqlalchemy import (
    create_engine, String, Integer, Float, ForeignKey, MetaData, Table, inspect, select
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
import time
import pandas as pd


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