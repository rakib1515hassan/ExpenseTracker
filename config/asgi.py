"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application
import os

import dotenv
import environ

env = environ.Env()
env.read_env()





# dotenv.load_dotenv(os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE')))


django_setting = env('DJANGO_SETTINGS', default='local')


if django_setting == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

elif django_setting == 'local':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = get_asgi_application()
