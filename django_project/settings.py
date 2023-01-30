from pathlib import Path

from environs import Env


env = Env()
env.read_env()

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ROLLBAR = {
    "access_token": env.str("ROLLBAR_ACCESS_TOKEN"),
    "environment": "development" if DEBUG else "production",
    "code_version": "1.0",
    "root": BASE_DIR,
}

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "45.95.234.132",
]

if DEBUG:
    # Config internal ips for DjDT with Docker Compose
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

CSRF_TRUSTED_ORIGINS = [
    "http://*.127.0.0.1",
    "http://45.95.234.132",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Must be above "django.contrib.staticfiles"
    "django.contrib.staticfiles",
    # 3rd party apps
    "crispy_forms",
    "crispy_bootstrap5",
    "notifications",
    "debug_toolbar",
    "django_bleach",
    # Local
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "journal.apps.JournalConfig",
    "documents.apps.DocumentsConfig",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # 3rd
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 3rd
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_project.rollbar_middleware.CustomRollbarNotifierMiddleware",  # 3rd
]

ROOT_URLCONF = "django_project.urls"

TEMPLATES = [
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
                # Local
                "journal.context_processors.green_tasks",
                "documents.context_processors.green_documents",
            ],
        },
    },
]

WSGI_APPLICATION = "django_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = "users.CustomUser"
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = env.str("STATIC_ROOT", "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# This is for uploads:
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login / logout stuff

LOGIN_REDIRECT_URL = "journal:task_list"
LOGOUT_REDIRECT_URL = "login"
SESSION_COOKIE_AGE = 60 * 60 * 16

# Crispy stuff
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django Notifications stuff
NOTIFICATIONS_NOTIFICATION_MODEL = "core.Notification"

# Django Bleach stuff
# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = ["p", "b", "i", "u", "em", "strong", "a", "code"]

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ["href", "title", "style"]

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [
    "font-family", "font-weight", "text-decoration", "font-variant"
]

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False
