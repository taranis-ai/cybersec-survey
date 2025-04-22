import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cybersec_survey.db.models import Base, NewsItem

DB_PATH = "sqlite:///database.db"
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    existing = session.query(NewsItem).count()

    if existing == 0:
        news_item_path = os.path.join(os.path.dirname(__file__), "..", "data", "news_items.yaml")
        with open(news_item_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            for news_item in data.get("news_items", []):
                session.add(NewsItem(content=news_item.get("content", ""), language=news_item.get("language", "")))
        session.commit()
        print("✅ Database initialized from defaults.")
    else:
        print("ℹ️ Database already initialized. Skipping seeding.")
    session.close()
