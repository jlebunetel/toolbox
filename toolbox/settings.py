"""Django settings for toolbox project."""
from logging.config import dictConfig
from pathlib import Path
from typing import Any

from django.core.management.utils import get_random_secret_key
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Load settings from environment variables or secrets files."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    debug: bool = False
    secret_key: str = Field(default_factory=get_random_secret_key)
    allowed_hosts: list[str] = [".localhost", "127.0.0.1", "[::1]"]
    language_code: str = "en"


settings = Settings()

DEBUG: bool = settings.debug
SECRET_KEY: str = settings.secret_key
ALLOWED_HOSTS: list[str] = settings.allowed_hosts
BASE_DIR: Path = Path(__file__).resolve().parent.parent
ROOT_URLCONF: str = "toolbox.urls"
WSGI_APPLICATION: str = "toolbox.wsgi.application"

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

DATABASES: dict[str, Any] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE: str = settings.language_code
TIME_ZONE: str = "UTC"
USE_I18N: bool = True
USE_TZ: bool = True

STATIC_URL: str = "static/"
STATIC_ROOT: Path = BASE_DIR / "static"

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL: str = "landing"
LOGOUT_REDIRECT_URL: str = "landing"

LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
            "%(process)d %(thread)d"
            "%(pathname)s %(lineno)d"
            "%(status_code)d %(request)s"
            "%(duration)f %(sql)s %(params)s %(alias)s"
            "%(receiver)s %(err)s",
        },
        "rich": {
            "format": '[%(process)d] "%(name)s" \n%(message)s',
        },
    },
    "handlers": {
        "json": {
            "class": "logging.StreamHandler",
            "filters": ["require_debug_false"],
            "formatter": "json",
        },
        "null": {
            "class": "logging.NullHandler",
        },
        "rich_console": {
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true"],
            "formatter": "rich",
            "rich_tracebacks": True,
        },
    },
    "root": {
        "level": "NOTSET",
        "handlers": [
            "json",
            "rich_console",
        ],
    },
    "loggers": {
        "django": {"level": "NOTSET"},
        "django.db.backends": {"level": "INFO"},
        "django.dispatch": {"level": "WARNING"},
        "django.request": {"level": "WARNING"},
        "django.security.DisallowedHost": {"handlers": ["null"], "propagate": False},
        "django.server": {"level": "WARNING"},
        "django.template": {"level": "WARNING"},
        "django.utils.autoreload": {"level": "INFO"},
    },
}
LOGGING_CONFIG: Any = None
dictConfig(LOGGING)
