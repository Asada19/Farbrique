from django.utils import timezone
from datetime import timedelta
from django.test import TestCase

from notification.models import Mailing, Client, Message

from notification.tasks import start_message
from notification.notify import send_mailing_message

from celery import shared_task


class MessageTestCase(TestCase):

    def setUp(self):
        self.client1 = Client.objects.create(phone_number='1234567890', code_operator='12345', tag='подписчики',
                                             timezone='UTC')
        self.client2 = Client.objects.create(phone_number='9876543210', code_operator='54321', tag='другой тег',
                                             timezone='Europe/Moscow')

    def test_send_mailing_message(self):
        mailing = Mailing.objects.create(
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1),
            text="Тестовое сообщение",
            filter_client={"tag": ["подписчики"], "operator_code": ["12345"]},
            time_interval=timedelta(minutes=30)
        )

        message = Message.objects.create(client=self.client1, mailing=mailing)

        task = send_mailing_message(message.id, self.client1.phone_number, mailing.text)
        self.assertTrue(task.status_code, 200)

    def test_mailing_time_interval(self):
        mailing = Mailing.objects.create(
            start_time=timezone.now() - timedelta(hours=3),
            end_time=timezone.now() - timedelta(hours=2),
            text="Тестовое сообщение",
            filter_client={"tag": ["подписчики"], "operator_code": ["12345"]},
            time_interval=timedelta(minutes=30)
        )
        task = start_message.apply_async(args=[mailing.id])
        self.assertFalse(task.successful())


class CeleryTestCase(TestCase):
    def test_start_message(self):
        task = start_message.s(mailing_id=1)
        result = task.apply()
        self.assertTrue(result.successful())
