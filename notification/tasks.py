import pytz
from django.utils import timezone
from celery import shared_task
from datetime import datetime
from django.conf import settings
from .notify import send_mailing_message, create_message, filter_clients


@shared_task
def start_message(mailing_id):
    print('get task')
    import logging
    from notification.models import Mailing, Client, Message
    message_logger = logging.getLogger('message')

    try:
        print('start recieve')
        mailing = Mailing.objects.get(id=mailing_id)
        current_time = timezone.now()

        if not mailing.start_time <= current_time <= mailing.end_time:
            print('this is will not work')
            return  # Exit if current time is within the mailing window

        clients = filter_clients(mailing)
        for client in clients:
            message = create_message(mailing_id=mailing.id, client_id=client.id)
            response = send_mailing_message(message_id=message.id,
                                            phone_number=client.phone_number,
                                            text=mailing.text)
            if response.status_code == 200:
                message.status = 'SENT'
                message_logger.info({'id': message.id,
                                     'method': 'UPDATE',
                                     'status': message.status,
                                     'client_id': client.id,
                                     'mailing_id': mailing.id
                                     })
                message.save()
            else:
                start_message.apply_async((mailing_id,), countdown=180)

        if current_time <= mailing.start_time:
            start_message.apply_async((mailing_id,), eta=mailing.start_time)
    except Mailing.DoesNotExist:
        pass


@shared_task
def send_statistic_to_mail():
    from django.core.mail import EmailMultiAlternatives, send_mail
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from notification.models import Mailing, Message

    subject = f'Статистика рассылок за {datetime.now()}'
    mailings = Mailing.objects.all()
    count = len(mailings)
    data = []
    for mail in mailings:
        msg = Message.objects.filter(mailing=mail).all()
        sent = len(msg.filter(status='SENT'))
        no_sent = len(msg.filter(status='NOT_SENT'))
        res = f'Рассылка  id: {mail.id}, время запуска: {mail.start_time} - время окончания: {mail.end_time} \n'\
              f'    Сообщения: {len(msg)}; Доставлено: {sent}; Не доставлено: {no_sent};'
        data.append(res)
    context = {
        'mailings_count': count,
        'messages': data
    }
    html_content = render_to_string(template_name='notification/notification_statistic.html', context=context)
    text_content = strip_tags(html_content)
    send_mail(subject, text_content, settings.FROM_MAIL, [settings.EMAIL_HOST_USER], fail_silently=True)
