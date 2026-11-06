from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    portal_url: str = "https://urja-ops.flockenergy.tech"
    portal_username: str = ""
    portal_password: str = ""
    request_timeout: float = 15.0

    class Config:
        env_file = ".env"


settings = Settings()
