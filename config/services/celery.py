import os

from config.env import env
from celery.schedules import crontab, schedule
from datetime import timedelta

# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Dhaka"
# timezone = "Asia/Dhaka"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# broker_connection_retry_on_startup = True


##* Set Broker Url
# To check redis url, go to the command line and run >> redis-cli
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
# broker_url = env('CELERY_BROKER_URL')




##* Set Result Backend
# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
# result_backend = env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

CELERY_RESULT_BACKEND = 'django-db'          ##! For Database
# result_backend  = 'django-db'              ##! For Database
# CELERY_CACHE_BACKEND   = 'django-cache'    ##! For Cache 
# result_backend = 'django-cache'


##* Result এর মধ্যে Task Name, args, kwargs, worker, retries, queue and delivery_info দেখাতে এটি ব্যবহার করা হয়।
CELERY_RESULT_EXTENDED = True



##* Periodic Task 
CELERY_BEAT_SCHEDULE = {
    # 'clear-session-cache-every-10-seconds':{
    #     "task": "apps.demo.task.clear_session_cache",
    #     "schedule": 10.0,  # Schedule to run every 10 seconds
    #     # "args": ('11111', ),
    # },

    'clear-task-backend-data-every-1-minute': {
        'task': 'apps.demo.task.clear_task_backend_data',  # Adjust the import path to your task
        'schedule': crontab(minute='*/1'),         # Every 1 minute

        # 'schedule': crontab(minute=0, hour='*/2'),  #? প্রতি ২ ঘন্টা পর পর
        # 'schedule': crontab(minute=30, hour=0),     #? প্রতি দিন রাত ১২:৩০AM
        # 'schedule': crontab(minute=0, hour=22),     #? প্রতি দিন রাত ১০:০০PM
        # 'schedule': schedule(run_every=timedelta(days=7)),      #? প্রতি ৭ দিন পর পর
        # 'schedule': crontab(day_of_month=1, hour=0, minute=0),  #? প্রতি মাসের প্রথম দিন রাত ১২:০০
        # 'schedule': crontab(day_of_month='last', hour=23, minute=59),  #? প্রতি মাসের শেষ দিন ১১:৫৯ PM
        # 'schedule': crontab(month_of_year=1, day_of_month=1, hour=0, minute=0),  #? প্রতি বছরের জানুয়ারি ১ তারিখ, রাত ১২:০০
        
    },
    ## Add More Periodic task if you needed.
}




##* Additional Celery settings
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"




##* For AWS S3
# S3_ACCESS_KEY_ID = ''
# S3_SECRET_ACCESS_KEY = ''
# S3_BUCKET = ''
# S3_BASE_PATH = ''
# S3_ENDPOINT_URL = ''
# S3_REGION = ''


