import http

from rest_framework import generics
from rest_framework.response import Response
from notification.serializers import NewsletterSerializer, ClientSerializer, MessageSerializer, StatisticSerializer, GeneralStatisticSerializer
from notification.services import NewsletterService, ClientService, MessageService
from .models import Newsletter, Client, Message


class NewsletterAPIView(generics.ListCreateAPIView):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    service = NewsletterService


class Statistic(generics.ListAPIView):
    service = NewsletterService
    serializer_class = StatisticSerializer

    def get_queryset(self):
        data = self.service.general_statistic()
        return data


class DetailStatistic(generics.RetrieveAPIView):

    serializer_class = StatisticSerializer
    queryset = Newsletter.objects.all()
    service = NewsletterService

    def get_queryset(self):
        data = self.service.detail_statistic(self.request.data.get('pk'))
        return data


class NewsletterRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    service = NewsletterService


class ClientAPIView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    service = MessageService

