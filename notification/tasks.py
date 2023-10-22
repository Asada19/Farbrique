import pytz
from celery import shared_task
from datetime import datetime
from .notify import send_mailing_message, create_message, filter_clients
from celery import shared_task
from django.conf import settings


@shared_task
def create_task(mailing_id) -> None:
    from notification.models import Mailing, Client

    mailing = Mailing.objects.get(id=mailing_id)
    time_now = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE))

    if time_now >= mailing.start_time >= mailing.end_time:
        clients = filter_clients(mailing)
        for client in clients:
            message = create_message(mailing_id=mailing.id, client_id=client.id)
            response = send_mailing_message(message_id=message.id,
                                            phone_number=client.phone_number,
                                            text=mailing.text)
            print(response)
            if response.status_code == 200:
                message.status = 'SENT'
                message.save()
            else:
                create_task.apply_async((mailing, ), countdown=180)

    elif time_now < mailing.start_time:
        create_task.apply_async((mailing,), eta=mailing.start_time)
