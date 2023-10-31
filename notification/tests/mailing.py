from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notification.models import Mailing, Client
from notification.serializers import MailingSerializer


class MailingAPITestCase(APITestCase):

    def setUp(self):
        self.mailing_1 = Mailing.objects.create(start_time=timezone.now(), end_time='2024-10-23T00:00:00Z',
                                                text='test 1', filter_client={'tag': ['test'], 'code_operator': []})
        self.mailing_2 = Mailing.objects.create(start_time=timezone.now(), end_time='2024-10-23T00:00:00Z',
                                                text='test 2', filter_client={'tag': ['test'], 'code_operator': []})
        self.client_1 = Client.objects.create(phone_number='70000000000', tag='test', timezone='Asia/Bishkek')
        self.client_2 = Client.objects.create(phone_number='70000000001', tag='test', timezone='Asia/Bishkek')

    def test_get_mailings(self):
        url = reverse('mailing-list')
        response = self.client.get(url)
        mailings = Mailing.objects.all()
        serializer = MailingSerializer(mailings, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mailing_detail(self):
        url = reverse('mailing-detail', args=[self.mailing_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_mailing(self):
        data = {
            'start_time': timezone.now(),
            'text': 'test 3',
            'filter_client': {'tag': ['test'], 'code_operator': []}
        }
        url = reverse('mailing-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mailing.objects.count(), 3)
        self.assertEqual(Mailing.objects.get(id=3).text, data['text'])

    def test_update_mailing(self):
        data = {
            'text': 'New text'
        }
        url = reverse('mailing-detail', args=[self.mailing_1.id])
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mailing_1.refresh_from_db()
        self.assertEqual(self.mailing_1.text, data['text'])

    def test_delete_mailing(self):
        url = reverse('mailing-detail', args=[self.mailing_1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mailing.objects.count(), 1)
        self.assertEqual(Mailing.objects.filter(id=self.mailing_1.id).count(), 0)

    def test_general_statistic(self):
        url = reverse('mailing-general-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_statistic(self):
        url = reverse('mailing-detail-statistics', args=[self.mailing_1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)