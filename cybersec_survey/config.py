from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATA_PATH: str = ""
    DB_NAME: str = "survey_data.db"
    DEFAULT_NEWS_ITEM_FILE: str = "default_news_items.json"

    @field_validator("DATA_PATH", "DB_PATH", "DEFAULT_NEWS_ITEM_FILE", mode="before")
    def check_non_empty_string(cls, value: str, info: ValidationInfo) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{info.field_name} must be a non-empty string")
        return value


Config = Settings()
