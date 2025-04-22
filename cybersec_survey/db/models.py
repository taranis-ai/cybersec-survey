from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class NewsItem(Base):
    __tablename__ = "news_items"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    language = Column(String, nullable=False)


class ClassificationResult(Base):
    __tablename__ = "classifications"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    news_item_id = Column(Integer, ForeignKey("news_items.id"), nullable=False)
    cybersecurity = Column(String, nullable=False)
