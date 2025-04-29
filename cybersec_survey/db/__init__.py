from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cybersec_survey.db.models import Base, NewsItem
from cybersec_survey.config import Config
from pathlib import Path
import pandas as pd

DB_PATH = f"sqlite:///{Config.DATA_PATH}/{Config.DB_NAME}"
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    existing = session.query(NewsItem).count()

    if existing == 0:
        default_news_items_path = Path(Config.DATA_PATH) / Config.DEFAULT_NEWS_ITEM_FILE
        data_df = pd.read_json(default_news_items_path)
        for _, row in data_df.iterrows():
            session.add(
                NewsItem(
                    id=row["news_item_id"],
                    story_id=row["id"],
                    title=row["title"],
                    content=row["content"],
                    language=row["language"],
                    tokens=row["tokens"],
                )
            )
        session.commit()
        print("✅ Database initialized from defaults.")
    else:
        print("ℹ️ Database already initialized. Skipping seeding.")
    session.close()
