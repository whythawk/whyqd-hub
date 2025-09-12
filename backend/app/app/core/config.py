import secrets
from typing import List, Optional, Union
from typing_extensions import Self

from pydantic import (
    field_validator,
    AnyHttpUrl,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    TOTP_SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 90
    JWT_ALGO: str = "HS512"
    TOTP_ALGO: str = "SHA-1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    SERVER_BOT: str = "Symona"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    # https://stackoverflow.com/a/70657621/295606
    # Set to 1Mb ... Starlette has 1Mb as default, so only use this if different
    CHUNK_SIZE: int = 1024 * 1024

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @field_validator("SENTRY_DSN", mode="before")
    @classmethod
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    # GENERAL SETTINGS

    MULTI_MAX: int = 20

    # COMPONENT SETTINGS

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_TO_EMAIL: Optional[EmailStr] = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.SMTP_PORT and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = True

    # WHYQD KEYS
    # 10**9 == 1gb ==> try 16gb? 16000000000 dev_shm must be aligned in docker-compose, currently 8611409920
    # ray uses bytes -> gigabytes
    WHYQD_MEMORY: int = 6000000000  # 67104768
    WHYQD_CPUS: int = 3
    WHYQD_SPILLWAY: str = "/app/tmp/spill"
    WHYQD_DIRECTORY: str = "/app/working/tmp"
    WHYQD_DEFAULT_MIMETYPE: str = "application/vnd.apache.parquet"
    WHYQD_SUMMARY_ROWS: int = 50

    # PAYMENT KEYS
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_PUBLIC_KEY: Optional[str] = None
    STRIPE_WEBHOOK: Optional[str] = None
    STRIPE_MINIMUM_CHARGE_AMOUNT: Optional[int] = None
    USE_STRIPE: bool = False

    @model_validator(mode="after")
    def _get_use_stripe(self) -> Self:
        self.USE_STRIPE = bool(self.STRIPE_API_KEY and self.STRIPE_PUBLIC_KEY and self.STRIPE_WEBHOOK)
        return self

    # WORKING WITH REFERENCES
    WORKING_PATH: str = "/app/working"
    REFERENCE_PATH: str = "/references"
    SUMMARY_PATH: str = "/summary"

    # DIGITALOCEAN SPACES KEYS
    SPACES_ACCESS_KEY: Optional[str] = None
    SPACES_SECRET_KEY: Optional[str] = None
    SPACES_REGION_NAME: Optional[str] = None
    SPACES_ENDPOINT_URL: Optional[HttpUrl] = None
    SPACES_BUCKET: Optional[str] = None
    USE_SPACES: bool = False

    @model_validator(mode="after")
    def _get_use_spaces(self) -> Self:
        self.USE_SPACES = bool(
            self.SPACES_ACCESS_KEY
            and self.SPACES_SECRET_KEY
            and self.SPACES_REGION_NAME
            and self.SPACES_ENDPOINT_URL
            and self.SPACES_BUCKET
        )
        return self

    # IP2LOCATION IP COUNTRY LOCATION
    IP2_LINK: HttpUrl = "https://www.ip2location.com/download/"
    IP2_FOLDER: Optional[str] = None
    IP2_BIN_FILE: str = "IP2LOCATION-LITE-DB1.BIN"
    IP2_TOKEN: Optional[str] = None
    IP2_FILE: Optional[str] = None
    IP2_FILE_IPV6: Optional[str] = None
    IP2_ENDPOINT_URL: Optional[HttpUrl] = None
    USE_IP2: bool = False
    EURO_CURRENCY: List[str] = [
        "AT",
        "BE",
        "BG",
        "CH",
        "CY",
        "CZ",
        "DE",
        "DK",
        "EE",
        "ES",
        "FI",
        "FR",
        "GR",
        "HR",
        "HU",
        "IE",
        "IS",
        "IT",
        "LI",
        "LT",
        "LU",
        "LV",
        "MT",
        "NL",
        "NO",
        "PL",
        "PT",
        "RO",
        "SE",
        "SI",
        "SK",
    ]

    @model_validator(mode="after")
    def _get_ip2_endpoint_url(self) -> Self:
        self.IP2_ENDPOINT_URL = f"{self.IP2_LINK}?token={self.IP2_TOKEN}&file={self.IP2_FILE}"
        return self

    @model_validator(mode="after")
    def _get_use_ip2(self) -> Self:
        self.USE_IP2 = bool(self.IP2_TOKEN and self.IP2_LINK and self.IP2_FILE)
        return self

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
