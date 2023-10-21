from django.contrib import admin
from .models import Newsletter, Client, Message


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', )

