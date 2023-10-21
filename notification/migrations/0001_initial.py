# Generated by Django 4.2.6 on 2023-10-21 00:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('code_operator', models.CharField(max_length=5)),
                ('tag', models.CharField(max_length=10)),
                ('timezone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('text', models.TextField()),
                ('filter_client', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('SENT', 'SENT'), ('NOT SENT', 'NOT_SENT')], max_length=10)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='notification.client')),
                ('newsletter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='notification.newsletter')),
            ],
        ),
    ]