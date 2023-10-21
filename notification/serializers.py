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

    def create(self, validated_data):
        messages = validated_data.pop('message')
        newsletter = Newsletter.objects.create(**validated_data)
        for message in messages:
            Message.objects.create(**message)
        return newsletter

    def update(self, instance, validated_data, partial=True):
        messages_data = validated_data.pop('message')
        messages = list(instance.message.all())
        for message_data in messages_data:
            message = messages.pop(0)
            message.status = message_data.get('status', message.status)
            message.client = message_data.get('client', message.client)
            message.save()
        newsletter = instance

        newsletter.end_time = validated_data.get('end_time', newsletter.end_time)
        newsletter.text = validated_data.get('text', newsletter.text)
        newsletter.filter_client = validated_data.get('filter_client', newsletter.filter_client)
        newsletter.save()
        return instance


class NewsletterRetrieveSerializer(NewsletterSerializer):
    message = MessageSerializer(many=True)


class ClientSerializer(serializers.ModelSerializer):
    message = MessageSerializer(many=True)

    class Meta:
        model = Client
        fields = '__all__'


class StatisticSerializer(serializers.Serializer):
    newsletter = serializers.CharField()
    messages = MessageSerializer(read_only=True, many=True)
    count_of_sent = serializers.IntegerField()
    count_of_not_sent = serializers.IntegerField()

