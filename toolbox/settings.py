"""Django settings for toolbox project."""

import sys
from logging.config import dictConfig
from pathlib import Path
from typing import Any

from django.core.management.utils import get_random_secret_key
from django.forms.renderers import TemplatesSetting
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomFormRenderer(TemplatesSetting):
    """Customize the default form renderer."""

    form_template_name = "forms/base.html"


class Settings(BaseSettings):
    """Load settings from environment variables or secrets files."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    debug: bool = False
    secret_key: str = Field(default_factory=get_random_secret_key)
    allowed_hosts: list[str] = [".localhost", "127.0.0.1", "[::1]"]
    language_code: str = "en"

    site_domain: str = "example.com"
    site_name: str = "My Toolbox"

    superuser_username: str = "demo"
    superuser_password: str = "demo"
    superuser_email: str = "demo@example.com"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"


settings = Settings()

DEBUG: bool = settings.debug
SECRET_KEY: str = settings.secret_key
ALLOWED_HOSTS: list[str] = settings.allowed_hosts
BASE_DIR: Path = Path(__file__).resolve().parent.parent
APPS_DIR: Path = BASE_DIR / "apps"
sys.path.append(str(APPS_DIR))
ROOT_URLCONF: str = "toolbox.urls"
WSGI_APPLICATION: str = "toolbox.wsgi.application"

SITE_ID: int = 1
CUSTOM_SITE_DOMAIN: str = settings.site_domain
CUSTOM_SITE_NAME: str = settings.site_name

CUSTOM_SUPERUSER_USERNAME: str = settings.superuser_username
CUSTOM_SUPERUSER_PASSWORD: str = settings.superuser_password
CUSTOM_SUPERUSER_EMAIL: str = settings.superuser_email


INSTALLED_APPS: list[str] = [
    "accounts.apps.AccountsConfig",  # before django.contrib.auth to override templates
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
    "core.apps.CoreConfig",
    "allauth",
    "allauth.account",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "allauth.account.middleware.AccountMiddleware",
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
                "templates.context_processors.version",
            ],
        },
    }
]

DATABASES: dict[str, Any] = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": settings.postgres_host,
        "PORT": settings.postgres_port,
        "NAME": settings.postgres_db,
        "USER": settings.postgres_user,
        "PASSWORD": settings.postgres_password,
    }
}

AUTHENTICATION_BACKENDS: list[str] = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

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
AUTH_USER_MODEL: str = "accounts.User"

ACCOUNT_ADAPTER: str = "accounts.adapter.CustomUserAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD: str = "username_email"
ACCOUNT_CHANGE_EMAIL: bool = True

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS: int = 3
ACCOUNT_EMAIL_REQUIRED: bool = True
ACCOUNT_EMAIL_VERIFICATION: str = "mandatory"
ACCOUNT_FORMS: dict[str, str] = {"signup": "accounts.forms.CustomSignupForm"}
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION: bool = True
ACCOUNT_LOGOUT_REDIRECT_URL: str = "core:landing"
ACCOUNT_PRESERVE_USERNAME_CASING: bool = False
ACCOUNT_USERNAME_MIN_LENGTH: int = 6
ACCOUNT_USERNAME_VALIDATORS: str = "accounts.validators.username_validators"

LOGIN_REDIRECT_URL: str = "core:landing"
LOGOUT_REDIRECT_URL: str = "core:landing"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LANGUAGE_CODE: str = settings.language_code
TIME_ZONE: str = "UTC"
USE_I18N: bool = True
USE_TZ: bool = True

STATIC_ROOT: Path = BASE_DIR / "static"
STATIC_URL: str = "static/"

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

FORM_RENDERER = "toolbox.settings.CustomFormRenderer"

LOGGING_CONFIG: Any = None
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
        "handlers": ["json", "rich_console"],
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
        "psycopg.pq": {"level": "INFO"},
    },
}
dictConfig(LOGGING)
