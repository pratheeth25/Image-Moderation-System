from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# Get DB URL from environment (Render / Cloud)
DB_URL = os.getenv("DATABASE_URL")


# Safety check
if not DB_URL:
    raise ValueError("DATABASE_URL is not set in environment variables")


# Fix for Render: sometimes needs this
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)


engine = create_engine(
    DB_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class ImageLog(Base):

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    nsfw_score = Column(Float)
    violence_score = Column(Float)
    status = Column(String)


# Create tables
Base.metadata.create_all(bind=engine)
