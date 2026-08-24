from core.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , DeclarativeBase  , relationship , declared_attr , Session
from sqlalchemy import Column , Integer , String , DateTime , Boolean , Text , func ,ForeignKey , and_ , or_ , UniqueConstraint , Enum as SAEnum
from sqlalchemy.dialects.postgresql import ENUM
import uuid
from enum import Enum

def generate_public_id() -> str:
    raw = uuid.uuid4().hex
    parts = [raw[i:i+4] for i in range(0, 16, 4)]
    return "-".join(parts)

engine = create_engine(settings.setting.sqlalchemy_database_url , echo=False)
SeeseionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase) :
    pass


class BasicTabales (Base) :
    __abstract__ = True
    id = Column(Integer , primary_key=True , index=True)
    public_id = Column(String , unique=True , nullable=False , default=generate_public_id)
    create_at = Column(DateTime , nullable=False , default=func.now())

def get_db() :
    db = SeeseionLocal()
    try : 
        yield db
    finally :
        db.close()



class ByCompanyAndCreator (BasicTabales) :
    __abstract__ = True
    company_id = Column(Integer , ForeignKey("companys.id") , nullable=False)
    creator_id = Column(Integer , ForeignKey("partners.id") , nullable=False)