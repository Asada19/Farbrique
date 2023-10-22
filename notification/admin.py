from django.contrib import admin
from .models import Mailing, Client, Message


@admin.register(Mailing)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'start_time', 'end_time')
    list_display_links = ('id', 'text')
    list_filter = ('start_time', 'end_time', 'filter_client')
    search_fields = ('text', 'id')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'code_operator', 'phone_number', 'timezone', 'tag')
    list_display_links = ('id', 'code_operator', 'phone_number')
    list_filter = ('code_operator', 'timezone', 'tag')
    search_fields = ('id', 'phone_number')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'status')
    list_display_links = ('id', 'created_at', 'status')
    list_filter = ('created_at', 'status')
    search_fields = ('id', )
