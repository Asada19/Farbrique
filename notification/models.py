import uuid
from django.db import models


class Newsletter(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    filter_client = models.JSONField(default=dict)


class Client(models.Model):
    phone_number = models.CharField(max_length=15)
    code_operator = models.CharField(max_length=5)
    tag = models.CharField(max_length=10)
    timezone = models.CharField(max_length=15)


class Message(models.Model):
    STATUS = (
        ('SENT', "SENT"),
        ('NOT SENT', "NOT_SENT")
    )
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=10)
    news_letter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, related_name='message')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='message')



