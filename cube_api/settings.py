"""
Django settings for cube_api project.
"""

from pathlib import Path
import os
import environ 
from datetime import timedelta # NOUVEL IMPORT pour la durée de vie des tokens

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialisation et lecture du fichier .env
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Applications Django par défaut
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications tierces (pour l'API)
    'rest_framework', 
    'corsheaders',    
    'rest_framework_simplejwt', # CLÉ pour l'authentification par Token JWT

    # VOTRE APPLICATION 
    # Correction : Référence complète à la classe de configuration pour un chargement correct des modèles
    'core_api.apps.CoreApiConfig',
]

MIDDLEWARE = [
    # Middleware pour CORS (doit être placé très haut)
    'corsheaders.middleware.CorsMiddleware', 
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cube_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cube_api.wsgi.application'


# Database
DATABASES = {
    'default': env.db_url(
        'DATABASE_URL',
        default=f'postgres://{env("PG_USER")}:{env("PG_PASSWORD")}@{env("PG_HOST")}:{env("PG_PORT")}/{env("PG_DB_NAME")}'
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Modèle Utilisateur Personnalisé
# Doit correspondre exactement au nom de la classe dans core_api/models.py
AUTH_USER_MODEL = 'core_api.CustomUser' 


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'


# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True 

# -----------------------------------------------------
# CONFIGURATION DE L'API REST & JWT
# -----------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Définit JWT comme la méthode d'authentification par défaut
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Définit l'authentification requise par défaut pour tous les endpoints
        'rest_framework.permissions.IsAuthenticated',
    )
}

SIMPLE_JWT = {
    # Durée de vie du token d'accès
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    # Durée de vie du token de rafraîchissement
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    
    'USER_ID_FIELD': 'id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
}