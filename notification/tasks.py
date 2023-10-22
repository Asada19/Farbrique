import pytz
from celery import shared_task
from datetime import datetime
from .models import Mailing, Client
from .notify import send_mailing_message, create_message
from celery import shared_task
from django.conf import settings


@shared_task()
def create_task(mailing: Mailing, client: Client) -> None:
    time_now = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE))

    if time_now >= mailing.start_time >= mailing.end_time:
        message = create_message(mailing_id=mailing.id, client_id=client.id)
        phone_number = message.client.phone_number
        text = mailing.text
        response = send_mailing_message.delay(message_id=message.id, phone_number=phone_number, text=text)
        if response.status_code == 200:
            message.status = 'SENT'
            message.save()
        else:
            create_task.apply_async((client, mailing), countdown=180)

