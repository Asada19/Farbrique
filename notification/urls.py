from django.urls import path, include
from .views import ClientAPIView, NewsletterAPIView
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'mailing', NewsletterAPIView, basename='mailing')
router.register(r'clients', ClientAPIView, basename='clients')


urlpatterns = [
    path('', include(router.urls)),
]
