from rest_framework import generics
from rest_framework.response import Response
from notification.serializers import NewsletterSerializer, ClientSerializer, MessageSerializer
from notification.services import NewsletterService, ClientService, MessageService
from .models import Newsletter, Client, Message


class NewsletterAPIView(generics.ListCreateAPIView):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()


class NewsletterRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()


class ClientAPIView(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def statistic(self):
        ...


class ClientRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def statistic(self):
        ...


class MessageAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    service = MessageService

