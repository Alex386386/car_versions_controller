import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == False

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
    "rest_framework",
    "rest_framework.authtoken",
    "cars",
    "comments",
    "core",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.year.year",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"


if os.getenv("TESTING", "0") == "1":
    ROOT_URLCONF = "src.src.urls"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    ROOT_URLCONF = "src.urls"
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE"),
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{levelname}] ({asctime}) {module} - {process:d} {thread:d} : {message}",
                "style": "{",
            }
        },
        "handlers": {
            "django_file": {
                "level": "DEBUG",
                "formatter": "verbose",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/app/logs/django_logs.log",
                "maxBytes": 1024 * 1024 * 15,
                "backupCount": 3,
            },
            "api_file": {
                "level": "DEBUG",
                "formatter": "verbose",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/app/logs/api.log",
                "maxBytes": 1024 * 1024 * 15,
                "backupCount": 3,
            },
            "apps_file": {
                "level": "DEBUG",
                "formatter": "verbose",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "/app/logs/apps.log",
                "maxBytes": 1024 * 1024 * 15,
                "backupCount": 3,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["django_file"],
                "propagate": False,
            },
            "django.request": {
                "handlers": ["django_file"],
                "level": "ERROR",
                "propagate": False,
            },
            "api": {
                "handlers": ["api_file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "cars": {
                "handlers": ["apps_file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "comments": {
                "handlers": ["apps_file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "cars:index"

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
