from .base import *      # Import all files from the base directory


# SECRET_KEY = 'django-insecure-eqrvwi@5!59^qwp*wybrq)i8up-uko2n@@c=u+ym(!s3)f30a&'
SECRET_KEY = env('SECRET_KEY')


DEBUG = env.bool('DJANGO_DEBUG', default=True)


ALLOWED_HOSTS = ['*']


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

