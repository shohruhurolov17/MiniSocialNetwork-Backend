from celery.schedules import crontab
from django.conf import settings
from environs import env

env.read_env()


CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_TIMEZONE = env('CELERY_TIMEZONE')


CELERY_BEAT_SCHEDULE = {
    "delete_unverified_users_monthly": {
        "task": "apps.users.tasks.delete_unverified_users",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
     "delete_expired_articles_monthly": {
        "task": "apps.posts.tasks.delete_expired_articles",
        "schedule": crontab(day_of_month=1, hour=0, minute=10),
    },
}