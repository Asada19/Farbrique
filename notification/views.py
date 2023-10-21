from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from notification.serializers import NewsletterSerializer, ClientSerializer, MessageSerializer, StatisticSerializer
from notification.services import NewsletterService
from .models import Newsletter, Client, Message
from drf_yasg.utils import swagger_auto_schema


class NewsletterAPIView(viewsets.ModelViewSet):
    model = Newsletter
    serializer_class = NewsletterSerializer
    queryset = Newsletter.objects.all()
    service = NewsletterService

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

