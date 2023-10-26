import logging
from rest_framework.decorators import action
from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from notification.serializers import MailingSerializer, ClientSerializer, MessageSerializer, StatisticSerializer
from notification.services import MailingService
from .models import Mailing, Client, Message
from drf_yasg.utils import swagger_auto_schema


class NewsletterAPIView(viewsets.ModelViewSet):
    model = Mailing
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
    service = MailingService

    @action(detail=False, methods=['get'])
    def general_statistics(self, *args, **kwargs):
        data = self.service.general_statistic()
        response = StatisticSerializer(data, many=True).data
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def detail_statistics(self, *args, **kwargs):
        data = self.service.detail_statistic(pk=self.kwargs.get('pk'))
        response = StatisticSerializer(data).data
        return Response(response, status=status.HTTP_200_OK)


class ClientAPIView(viewsets.ModelViewSet):
    model = Client
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
