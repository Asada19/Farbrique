from rest_framework import serializers
from .models import Newsletter, Client, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True, required=False)

    class Meta:
        model = Newsletter
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'


class StatisticSerializer(serializers.Serializer):
    newsletter = serializers.CharField()
    message = MessageSerializer(read_only=True, many=True)
    count_of_sent = serializers.IntegerField()


class GeneralStatisticSerializer(serializers.Serializer):
    object = serializers.ListSerializer(child=StatisticSerializer(), read_only=True)


