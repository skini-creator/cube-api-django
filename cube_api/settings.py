"""
Django settings for cube_api project.
"""

from pathlib import Path
import os
import environ # Import pour gérer le fichier .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialisation et lecture du fichier .env
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY') # Utilisation de la clé du .env

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
    'rest_framework', # Ajout de Django Rest Framework
    'corsheaders',    # Ajout de CORS (si nécessaire pour le frontend)

    # VOTRE APPLICATION
    'core_api',       # Ajout de votre application 'core_api'
]

MIDDLEWARE = [
    # Middleware pour CORS (doit être placé très haut)
    'corsheaders.middleware.CorsMiddleware', # Ajout de CorsMiddleware
    
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
# Configuration PostgreSQL utilisant les variables du .env
DATABASES = {
    'default': env.db_url(
        'DATABASE_URL',
        # URL construite à partir des variables .env
        default=f'postgres://{env("PG_USER")}:{env("PG_PASSWORD")}@{env("PG_HOST")}:{env("PG_PORT")}/{env("PG_DB_NAME")}'
    )
}


# Password validation
# ... (laissez cette section telle quelle)

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
# Indique à Django d'utiliser votre modèle 'Client' comme modèle d'utilisateur principal
AUTH_USER_MODEL = 'core_api.Client' 


# Internationalization
# ... (laissez cette section telle quelle)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# ... (laissez cette section telle quelle)

STATIC_URL = 'static/'


# CORS Settings (Ajuster selon vos besoins en production)
CORS_ALLOW_ALL_ORIGINS = True 
# Si vous voulez restreindre, utilisez CORS_ALLOWED_ORIGINS = ['http://localhost:3000', 'https://votre-frontend.com']