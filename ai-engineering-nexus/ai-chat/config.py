from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic will automatically look for GOOGLE_API_KEY in your .env
    google_api_key: str 
    openrouter_api_key: str
    default_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file="../../.env", extra="ignore")

settings = Settings()