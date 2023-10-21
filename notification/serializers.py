from rest_framework import serializers
from .models import Newsletter, Client, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True)

    class Meta:
        model = Newsletter
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

