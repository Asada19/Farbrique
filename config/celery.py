import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('Notification_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_statistic_to_mail': {
        'task': 'notification.tasks.send_statistic_to_mail',
        'schedule': crontab(hour=12, minute=0),
    }
}
