from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(env_file=".env")


db_settings = DatabaseSettings()
DATABASE_URL = f"postgresql://{db_settings.db_user}:{db_settings.db_password}@{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_name}"
