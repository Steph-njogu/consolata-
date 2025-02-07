from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-secret-key')  # Use environment variable in production
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'channels',
    'taggit',
    'seminary',
    'users',
    'home',
    'blogs',
    'chat',
    'events',
    'admission',
    'timetable',
    'course',
    'studentportal',
    'django_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'seminaryproject.urls'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',  
            ],
        },
    },
]


WSGI_APPLICATION = 'seminaryproject.wsgi.application'
ASGI_APPLICATION = "seminaryproject.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'steph',  # Use the correct database name
        'USER': 'steph',  # Use the correct user
        'PASSWORD': 'steph124en',  # Use the correct password
        'HOST': 'localhost',  # Default localhost connection
        'PORT': '5433',  # PostgreSQL port (keep as is)
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
LANGUAGES = [("en", _("English")), ("es", _("Spanish")), ("fr", _("French")), ("de", _("German"))]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Africa/Nairobi'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication settings
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'users:home'
LOGOUT_REDIRECT_URL = 'users:login'

# Email backends
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
AUTHENTICATE_BACKEND = ['django.contrib.auth.backends.ModelBackend', 'users.authentication.EmailAuthBackend']

