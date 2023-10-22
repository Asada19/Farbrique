import uuid
from django.db import models


class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name="время запуска рассылки")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="время окончания рассылки")
    text = models.TextField(verbose_name="текст сообщения")
    filter_client = models.JSONField(default=dict, verbose_name="фильтр клиентов")

    def __str__(self):
        return f'Mailing id: {self.id}, text: {self.text}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = verbose_name
        ordering = ['-start_time']


class Client(models.Model):
    phone_number = models.CharField(max_length=15, verbose_name='номер телефона')
    code_operator = models.CharField(max_length=5, verbose_name='код оператора')
    tag = models.CharField(max_length=10, verbose_name='тэг')
    timezone = models.CharField(max_length=15, verbose_name='часовой пояс')

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = verbose_name


class Message(models.Model):

    class Status(models.TextChoices):
        SENT = 'SENT', 'SENT'
        NOT_SENT = 'NOT_SENT', 'NOT_SENT'

    created_at = models.DateTimeField(auto_now=True, verbose_name='время создания')
    status = models.CharField(choices=Status.choices, default=Status.NOT_SENT, max_length=10, verbose_name='статус')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages',
                                verbose_name='рассылки', blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages', verbose_name='клиенты')

    def __str__(self):
        return f'{self.created_at}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = verbose_name

