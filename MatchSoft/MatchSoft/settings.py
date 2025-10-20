"""
Django settings for MatchSoft project (prod-ready for Render).
"""

import os
from pathlib import Path
from urllib.parse import urlparse
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Seguridad / Entorno
# -----------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS robusto: soporta variable por comas y host de Render
_raw_hosts = os.getenv("ALLOWED_HOSTS", "*.onrender.com,localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

# Render expone la URL pública; úsala si está disponible
render_external = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_external:
    # Si viene con esquema (https://...), extrae el hostname; si no, úsalo tal cual
    host = urlparse(render_external).hostname if "://" in str(render_external) else render_external
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

# CSRF_TRUSTED_ORIGINS debe incluir esquema (https://...)
_csrf = []
if render_external:
    # Normalmente RENDER_EXTERNAL_URL ya trae el esquema correcto
    url = render_external if "://" in str(render_external) else f"https://{render_external}"
    _csrf.append(url)
else:
    # Fallback: genera orígenes a partir de ALLOWED_HOSTS (solo https)
    _csrf = [f"https://{h}" for h in ALLOWED_HOSTS if h not in ("*",)]

CSRF_TRUSTED_ORIGINS = _csrf

# Si estás detrás de proxy (Render), respeta X-Forwarded-Proto para HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Endurece cookies en producción
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# -----------------------
# Apps
# -----------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

# -----------------------
# Middleware (WhiteNoise)
# -----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # sirve estáticos en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MatchSoft.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # opcional
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "MatchSoft.wsgi.application"

# -----------------------
# Base de datos
# -----------------------
# En Render usa DATABASE_URL (Postgres); en local, sqlite.
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# -----------------------
# Password validators
# -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------
# Internacionalización
# -----------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------
# Estáticos (WhiteNoise)
# -----------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
