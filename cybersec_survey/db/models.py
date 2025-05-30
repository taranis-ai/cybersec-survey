from enum import Enum

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
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
    username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    news_item_id = Column(String, ForeignKey("news_items.id", ondelete="CASCADE"), nullable=False)
    cybersecurity = Column(String, nullable=False)
    comment = Column(String, nullable=False)

    user = relationship("User", back_populates="classifications")
    news_item = relationship("NewsItem")


class Role(Enum):
    SCIENTIST = "Scientist"
    ENGINEER = "Engineer"
    MANAGER = "Project Manager"
    OTHER = "Other"


class Experience(Enum):
    NONE = "< 1 year"
    JUNIOR = "2-3 years"
    MID = "4-5 years"
    SENIOR = "5+ years"


class NewsFreq(Enum):
    SELDOM = "< 1 times per week"
    WEEKLY = "2-3 times per week"
    DAILY = "daily"


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    role = Column(SAEnum(Role, name="role_enum"), nullable=False)
    experience = Column(SAEnum(Experience, name="experience_enum"), nullable=False)
    news_freq = Column(SAEnum(NewsFreq, name="newsfreq_enum"), nullable=False)

    classifications = relationship("ClassificationResult", back_populates="user", cascade="all, delete-orphan")
