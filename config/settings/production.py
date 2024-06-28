from .base import *     # Import all files from the base directory

from config.env import env



SECRET_KEY = env('SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])



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