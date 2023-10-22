from rest_framework import serializers
from .models import Mailing, Client, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Mailing
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'


class StatisticSerializer(serializers.Serializer):
    mailing = serializers.CharField()
    count_of_sent = serializers.IntegerField()
    count_of_not_sent = serializers.IntegerField()

