from django.urls import path, include
from .views import ClientAPIView, MailingViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'mailing', MailingViewSet, basename='mailing')
router.register(r'clients', ClientAPIView, basename='clients')


urlpatterns = [
    path('', include(router.urls)),
]
