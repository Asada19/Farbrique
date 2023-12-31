# Generated by Django 4.2.6 on 2023-10-22 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='notification.client', verbose_name='клиенты'),
        ),
        migrations.AlterField(
            model_name='message',
            name='mailing',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='notification.mailing', verbose_name='рассылки'),
        ),
    ]
