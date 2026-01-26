from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "local"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_prefix="FINSENSE_",case_sensitive=False)

settings = Settings()
