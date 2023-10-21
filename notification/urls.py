from django.urls import path
from .views import ClientAPIView, ClientRetrieveAPIView, NewsletterAPIView, NewsletterRetrieveAPIView


urlpatterns = [
    path('client', ClientAPIView.as_view(), name='Client list-create'),
    path('client/<int:pk>', ClientRetrieveAPIView.as_view(), name='Client retrieve'),
    path('newsletter', NewsletterAPIView.as_view(), name='Newsletter list-create'),
    path('newsletter/<int:pk>', NewsletterRetrieveAPIView.as_view(), name='Newsletter retrieve'),
]
