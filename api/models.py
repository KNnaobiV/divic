import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column


Base = declarative_base()

def create_tables(engine):
    Base.metadata.create_all(engine, checkfirst=True)

class User(Base):
    __tablename__ = "daily"

    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created: Mapped[datetime.date] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    updated: Mapped[datetime.time] = mapped_column(nullable=True)
