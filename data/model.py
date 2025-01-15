from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float


Base = declarative_base()


class Usage(Base):
    __tablename__ = 'usage'

    id = Column(Integer, primary_key=True, index=True)
    cpu = Column(Float)
    ram = Column(Float)
    disk = Column(Float)
    