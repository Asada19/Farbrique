import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Mailing, Client
from .serializers import MailingSerializer, ClientSerializer


class MailingAPITestCase(APITestCase):

    def setUp(self):
        self.mailing_1 = Mailing.objects.create(start_time=datetime.datetime.now(), end_time='2024-10-23T00:00:00Z',
                                                text='test 1', filter_client={'tag': ['test'], 'code_operator': []})
        self.mailing_2 = Mailing.objects.create(start_time=datetime.datetime.now(), end_time='2024-10-23T00:00:00Z',
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
            'start_time': datetime.datetime.utcnow(),
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


class ClientAPITestCase(APITestCase):

    def setUp(self):
        self.client_1 = Client.objects.create(phone_number='70000000000', tag='test', timezone='Asia/Bishkek')
        self.client_2 = Client.objects.create(phone_number='70000000001', tag='test', timezone='Asia/Bishkek')

    def test_get_clients(self):
        response = self.client.get(reverse('clients-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_client(self):
        response = self.client.get(reverse('clients-detail', args=(self.client_1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], self.client_1.phone_number)
        self.assertEqual(response.data['tag'], self.client_1.tag)
        self.assertEqual(response.data['timezone'], self.client_1.timezone)
        self.assertEqual(response.data['code_operator'], self.client_1.code_operator)

    def test_create_client(self):
        response = self.client.post(reverse('clients-list'),
                                    data={'phone_number': '79999999997', 'tag': 'test', 'timezone': 'Asia/Bishkek',
                                          'code_operator': '999'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['phone_number'], '79999999997')
        self.assertEqual(response.data['tag'], 'test')
        self.assertEqual(response.data['timezone'], 'Asia/Bishkek')
        self.assertEqual(Client.objects.get(phone_number=response.data['phone_number']).code_operator, '999')

    def test_update_client(self):
        response = self.client.put(reverse('clients-detail', args=(self.client_1.id,)),
                                   data={'phone_number': '79999999997', 'tag': 'test', 'timezone': 'Asia/Bishkek',
                                         'code_operator': '999'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], '79999999997')
        self.assertEqual(response.data['tag'], 'test')
        self.assertEqual(response.data['timezone'], 'Asia/Bishkek')
        self.assertEqual(Client.objects.get(phone_number=response.data['phone_number']).code_operator, '999')

        response = self.client.patch(reverse('clients-detail', args=(self.client_1.id,)),
                                     data={'phone_number': '79999999991'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone_number'], '79999999991')
        self.assertEqual(response.data['tag'], 'test')
        self.assertEqual(response.data['timezone'], 'Asia/Bishkek')
        self.assertEqual(Client.objects.get(phone_number=response.data['phone_number']).code_operator, '999')

    def test_delete_client(self):
        response = self.client.delete(reverse('clients-detail', args=(self.client_1.id,)))
        self.assertEqual(response.status_code, 204)
        response = self.client.delete(reverse('clients-detail', args=(self.client_1.id,)))
        self.assertEqual(response.status_code, 404)

