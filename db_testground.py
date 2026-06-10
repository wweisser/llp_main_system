from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
if __name__ == "__main__":
    engine = create_engine('sqlite:///data_vault.db')
    metadata = MetaData()
    table_name = 'test_I'

    table = Table(table_name, metadata,

    inspect_engine(engine, table)
    remove_table(table, engine)
    inspect_engine(engine, table)


    conn = engine.connect()
    


    llp_table = Table(table, metadata,
        Column('id', Integer, primary_key=True),
        Column('case_number', Integer),
        Column('data', String),
        Column('timestamp', String)
    )

    # metadata.create_all(engine)
    # insert_data(engine, llp_table, 123, 'test data')
# termianl code: PRAGMA table_info(test);
# 
# Invoke-SqliteQuery -DataSource $db -Query "PRAGMA table_info(test_I);"