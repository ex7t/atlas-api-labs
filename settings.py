from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL, make_url


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    SQL_DSN: str | None = None
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "blog-local-password"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "blog_api"
    USERS_SQL_SCHEMA: str = Field(default="users", pattern=r"^[a-z_][a-z0-9_]{0,62}$")
    POSTS_SQL_SCHEMA: str = Field(default="post", pattern=r"^[a-z_][a-z0-9_]{0,62}$")
    SQL_ECHO: bool = False
    JWT_SECRET_KEY: SecretStr = Field(min_length=32)
    ACCESS_TOKEN_MINUTES: int = Field(default=15, ge=1, le=1440)
    REFRESH_TOKEN_DAYS: int = Field(default=7, ge=1, le=365)

    @property
    def database_url(self) -> URL:
        if self.SQL_DSN:
            return make_url(self.SQL_DSN)
        return URL.create(
            "postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


app_settings = AppSettings()
