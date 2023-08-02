from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    photo = Column(String)
    publish = Column(Boolean)
    created_at = Column(DateTime, default=func.now())

