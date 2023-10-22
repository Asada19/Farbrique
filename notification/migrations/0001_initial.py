# Generated by Django 4.2.6 on 2023-10-22 00:17

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
                ('phone_number', models.CharField(max_length=15, verbose_name='номер телефона')),
                ('code_operator', models.CharField(max_length=5, verbose_name='код оператора')),
                ('tag', models.CharField(max_length=10, verbose_name='тэг')),
                ('timezone', models.CharField(max_length=15, verbose_name='часовой пояс')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиент',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='время запуска рассылки')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='время окончания рассылки')),
                ('text', models.TextField(verbose_name='текст сообщения')),
                ('filter_client', models.JSONField(default=dict, verbose_name='фильтр клиентов')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылка',
                'ordering': ['-start_time'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='время создания')),
                ('status', models.CharField(choices=[('SENT', 'SENT'), ('NOT_SENT', 'NOT_SENT')], default='NOT_SENT', max_length=10, verbose_name='статус')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='notification.client', verbose_name='клиенты')),
                ('mailing', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='notification.mailing', verbose_name='рассылки')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщение',
            },
        ),
    ]
