from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Product Configuration API"
    admin_email: str = "admin@example.com"
    items_per_page: int = 10
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()