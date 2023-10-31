from django.urls import reverse
from rest_framework.test import APITestCase

from notification.models import Client


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
