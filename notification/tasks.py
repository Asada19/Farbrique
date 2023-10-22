import pytz
from celery import shared_task
from datetime import datetime
from django.conf import settings
from .notify import send_mailing_message, create_message, filter_clients


@shared_task
def start_message(mailing_id):
    from notification.models import Mailing, Client, Message

    try:
        mailing = Mailing.objects.get(id=mailing_id)
        current_time = datetime.now().astimezone(pytz.timezone(settings.TIME_ZONE))

        if mailing.start_time <= current_time <= mailing.end_time:
            return  # Exit if current time is within the mailing window

        clients = filter_clients(mailing)
        for client in clients:
            message = create_message(mailing_id=mailing.id, client_id=client.id)
            response = send_mailing_message(message_id=message.id,
                                            phone_number=client.phone_number,
                                            text=mailing.text)
            if response.status_code == 200:
                message.status = 'SENT'
                message.save()
            else:
                start_message.apply_async((mailing_id,), countdown=180)

        if current_time <= mailing.start_time:
            start_message.apply_async((mailing_id,), eta=mailing.start_time)
    except Mailing.DoesNotExist:
        pass
