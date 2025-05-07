from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", cli_parse_args=True)
    DATA_PATH: str = ""
    ADMIN_PW: str = "password"
    DB_NAME: str = "survey_data.db"
    DEFAULT_NEWS_ITEM_FILE: str = "default_news_items.json"
    PORT: int = 5306
    HOST: str = "0.0.0.0"
    DEBUG: bool = False


Config = Settings()
