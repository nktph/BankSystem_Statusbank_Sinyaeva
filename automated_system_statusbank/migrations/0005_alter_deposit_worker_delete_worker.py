# Generated by Django 4.0.4 on 2022-05-03 15:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('automated_system_statusbank', '0004_alter_deposittype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Worker',
        ),
    ]
