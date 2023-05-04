# Generated by Django 4.0.4 on 2022-05-03 15:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('automated_system_statusbank', '0005_alter_deposit_worker_delete_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='date_of_expire',
            field=models.DateField(default=datetime.datetime(2022, 5, 3, 15, 58, 33, 166047, tzinfo=utc), verbose_name='Дата окончания срока действия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deposit',
            name='date_of_issue',
            field=models.DateField(default=datetime.datetime(2022, 5, 3, 15, 59, 7, 379031, tzinfo=utc), verbose_name='Дата заключения договора'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deposit',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активен'),
        ),
    ]
