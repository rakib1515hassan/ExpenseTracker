#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Read.env file

def main():
    """Run administrative tasks."""

    django_setting =env('DJANGO_SETTINGS', default='local')

    # print("----------------------")
    # print(django_setting)
    # print("----------------------")

    if django_setting == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
        # print("=============")

    elif django_setting == 'local':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
        # print("++++++++++++++")

    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
        # print("*************")
        


    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

