"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from config.env import BASE_DIR, env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
env.read_env(os.path.join(BASE_DIR, '.env'))




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')




# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = env.bool('DJANGO_DEBUG', default=False)



ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])





## For Custom Apps Creat (apps/my_apps )
CUSTOM_APPS = [
    ##! For Admin Panel
    'apps.core.apps.CoreConfig',                  # core
    'apps.users.apps.UsersConfig',                # users
    'apps.dashboards.apps.DashboardsConfig',      # dashboards
]



## For Third Party Apps
THIRD_PARTY_APPS = [

    ## For Ckeditor
    # 'ckeditor', 
    # 'ckeditor_uploader',
    'django_cleanup.apps.CleanupConfig',
    
    # 'django_celery_beat',                        # For Celery Bit (Periodic Task)
    # 'django_celery_results',                     # For Celery Backend Results 


]



## Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
    "corsheaders",
    'django_extensions',

] + CUSTOM_APPS + THIRD_PARTY_APPS




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



## For Custom User Model
AUTH_USER_MODEL = 'users.User'
swappable = 'AUTH_USER_MODEL'



ROOT_URLCONF = 'config.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ##! For Admin Panel
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'apps/dashboards/templates'),
            os.path.join(BASE_DIR, 'apps/auth/templates'),

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



WSGI_APPLICATION = 'config.wsgi.application'




# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env('DB_NAME'),
#         "USER": env('DB_USER'),
#         "PASSWORD": env('DB_PASSWORD'),
#         "HOST": env('DB_HOST'),
#         "PORT": env('DB_PORT'),

#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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




# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REMEMBER_ME_EXPIRY = 60 * 60 * 24 * 30  # 30 days in seconds

OTP_TIMEOUT = 3  ## OTP timeout set 3 minutes




DEFAULT_PAGINATION_LIMIT = 2
FORM_RENDERER = 'config.forms.CustomDivFormRenderer'





##================= Package ===================================

from config.packege.jwt import *
from config.packege.drf import *






##================= Service ===================================

from config.services.email import *  
# from config.services.celery import * 




