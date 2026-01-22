from datetime import timedelta
from pathlib import Path
import os
from .loggin_formatters import CustomJsonFormatter

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # docs
    "drf_yasg",
    # libraries
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    # services
    "django_celery_beat",
    # apps
    "courses",
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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console_formater": {
            "format": "{asctime}|{levelname}|{module}|{message}",
            "style": "{",
        },
        "json_formater": {
            "()": CustomJsonFormatter,
        },
        "file_formater": {
            "format": "{asctime}|{levelname}|{module}|{message}",
            "style": "{"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console_formater",
        },
        "json_file": {
            "class": "logging.FileHandler",
            "formatter": "json_formater",
            "filename": BASE_DIR / "log" / "main.json",
        },
        "log_file": {
            "class": "logging.FileHandler",
            "formatter": "file_formater",
            "filename": BASE_DIR / "log" / "main.log",
        },
        "celery_file": {
            "class": "logging.FileHandler",
            "formatter": "file_formater",
            "filename": BASE_DIR / "log" / "celery.log",
        },
    },
    "loggers": {
        "users": {
            "handlers": ["console", "log_file"],
            "level": "INFO",
            "propagate": True,
        },
        "payment": {
            "handlers": ["console", "json_file", "log_file"],
            "level": "INFO",
            "propagate": True,
        },
        "celery_tasks": {
            "handlers": ["console", "celery_file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("NAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "HOST": os.getenv("HOST"),
        "PORT": os.getenv("PORT"),
    }
}

# Password validation
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
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

BASE_URL = os.getenv("BASE_URL")

STATIC_URL = "static/"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERY_TIMEZONE = TIME_ZONE

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    # 'task-name': {
    #     'task': 'vehicle.tasks.test_task',  # Путь к задаче
    #     'schedule': timedelta(minutes=10),  # Расписание выполнения задачи (например, каждые 10 минут)
    # },
}

# Email message sanding
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = os.getenv("APP_EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Secret data
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
