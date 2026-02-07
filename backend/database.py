from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://admin:admin123@localhost:5432/moderation"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ImageLog(Base):

    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    nsfw_score = Column(Float)
    violence_score = Column(Float)
    status = Column(String)


Base.metadata.create_all(engine)
