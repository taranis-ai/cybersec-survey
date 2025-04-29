from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from cybersec_survey.config import Config

DB_PATH = f"sqlite:///{Config.DATA_PATH}/{Config.DB_NAME}"
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class NewsItem(Base):
    __tablename__ = "news_items"
    id = Column(String, primary_key=True)
    story_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    language = Column(String, nullable=False)
    tokens = Column(Integer, nullable=False)


class ClassificationResult(Base):
    __tablename__ = "classifications"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    news_item_id = Column(String, ForeignKey("news_items.id"), nullable=False)
    cybersecurity = Column(String, nullable=False)
