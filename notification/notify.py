import os
import requests
import logging
from celery import shared_task
from django.db.models import Q, Count


@shared_task
def send_mailing_message(message_id: int, phone_number: str, text: str):
    service_url = f'https://probe.fbrq.cloud/docs#/send/{message_id}'
    access_token = os.environ.get('EXTERNAL_APP_ACCESS_TOKEN')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
    request_body = {
        "id": message_id,
        "phone": phone_number,
        "text": text,
    }
    return requests.post(service_url, json=request_body, headers=headers)


def create_message(mailing_id, client_id):
    import logging
    from notification.models import Mailing, Client, Message
    message_logger = logging.getLogger('message')

    client = Client.objects.get(id=client_id)
    mailing = Mailing.objects.get(id=mailing_id)
    message = Message.objects.create(client=client, mailing=mailing)
    message.save()
    message_logger.info({'id': message.id,
                         'method': 'Create',
                         'status': message.status,
                         'client_id': client_id,
                         'mailing_id': mailing_id
                         })
    return message


def filter_clients(mailing):
    from notification.models import Client

    tag = mailing.filter_client.get('tag')
    operator_code = mailing.filter_client.get('operator_code')
    filter_args = Q()

    if tag:
        filter_args &= Q(tag__in=tag)

    if operator_code:
        filter_args &= Q(operator_code__in=operator_code)
    clients = Client.objects.filter(filter_args)
    return clients
