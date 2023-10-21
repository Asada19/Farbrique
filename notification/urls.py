from django.urls import path
from .views import ClientAPIView, ClientRetrieveAPIView, NewsletterAPIView, NewsletterRetrieveAPIView, \
    Statistic, DetailStatistic

urlpatterns = [
    path('client', ClientAPIView.as_view(), name='Client list-create'),
    path('client/<int:pk>', ClientRetrieveAPIView.as_view(), name='Client retrieve'),
    path('newsletters', NewsletterAPIView.as_view(), name='Newsletter list-create'),
    path('statistic/', Statistic.as_view(), name='general statistic'),
    path('statistic/<int:pk>/', DetailStatistic.as_view(), name='detail statistic'),
    path('newsletter/<int:pk>/', NewsletterRetrieveAPIView.as_view(), name='Newsletter retrieve'),
]
