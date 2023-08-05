import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


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

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
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
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAILS_TO_EMAIL: Optional[EmailStr] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(values.get("SMTP_HOST") and values.get("SMTP_PORT") and values.get("EMAILS_FROM_EMAIL"))

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = True

    # WHYQD KEYS
    # 10**9 == 1gb ==> try 16gb? 16000000000 dev_shm must be aligned in docker-compose, currently 8611409920
    WHYQD_MEMORY: int = 6000000000
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

    @validator("USE_STRIPE", pre=True)
    def get_use_stripe(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(values.get("STRIPE_API_KEY") and values.get("STRIPE_PUBLIC_KEY") and values.get("STRIPE_WEBHOOK"))

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

    @validator("USE_SPACES", pre=True)
    def get_use_spaces(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SPACES_ACCESS_KEY")
            and values.get("SPACES_SECRET_KEY")
            and values.get("SPACES_REGION_NAME")
            and values.get("SPACES_ENDPOINT_URL")
            and values.get("SPACES_BUCKET")
        )

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

    @validator("IP2_ENDPOINT_URL", pre=True)
    def get_ip2_endpoint_url(cls, v: str, values: Dict[str, Any]) -> str:
        return f"{values.get('IP2_LINK')}?token={values.get('IP2_TOKEN')}&file={values.get('IP2_FILE')}"

    @validator("USE_IP2", pre=True)
    def get_use_ip2(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(values.get("IP2_TOKEN") and values.get("IP2_LINK") and values.get("IP2_FILE"))

    class Config:
        case_sensitive = True


settings = Settings()
