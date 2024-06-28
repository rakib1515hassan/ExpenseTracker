from __future__ import absolute_import, unicode_literals
import os

from config.env import env
from celery import Celery
from django.conf import settings

django_setting =env('DJANGO_SETTINGS', default='local')


## Set the default Django settings module for the 'celery' program.

if django_setting == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

elif django_setting == 'local':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')


app = Celery('config')

app.conf.enable_utc = False  ## By default it not set the timezone because i set my timezone
app.conf.update(timezone = 'Asia/Dhaka')





# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

# app.config_from_object("django.conf:settings", namespace="CELERY")
app.config_from_object(settings, namespace='CELERY')






# Load task modules from all registered Django apps.
app.autodiscover_tasks()



# print("+++++++++++++++++++++++++")
# print(f"CELERY_RESULT_BACKEND: {settings.CELERY_RESULT_BACKEND}")
# print("+++++++++++++++++++++++++")




@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print("+++++++++++++++++++++++++")
    print(f'Request: {self.request!r}')
    print("+++++++++++++++++++++++++")





##! For Periodic Task Management
from time import sleep
from datetime import timedelta
from celery.schedules import crontab

# app.conf.beat_schedule = {
#         'every-10-seconds':{
#         'task':'apps.demo.task.Test_Notification_Send',
#         # 'schedule':10,                        # Every 10 second
#         'schedule':timedelta(seconds=10),       # Every 10 second
#         # 'schedule': crontab(minute='*/1'),    # Every 1 minute
#         'args':('11111', )
#     }
#     # Add more periodic tasks as needed
# }








""" NOTE:- To install Celery, you need to install

    * Installing Redis

        >> pip install redis 
            or,
        >> pip install django-redis
            or,
        >> pip install "redis[hiredis]"   #!For faster performance,

    * Installation Celery

        >> pip install celery


    ! To check redis status
    >> sudo service redis status

    ! To check redis URL
    >> redis-cli
    >> ping

    ! To start celery worker
    >> python3 -m celery -A config worker -l info

    ! For Debug mode
    >> celery -A config worker -l debug

    ! For Start Celery Beat
    >> celery -A config beat -l info
    

"""