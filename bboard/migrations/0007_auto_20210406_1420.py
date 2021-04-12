# Generated by Django 3.1.7 on 2021-04-06 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0006_auto_20210406_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='title',
            field=models.CharField(error_messages={'blank': 'Название объявления отсутствует. Пожалуйста, введите название объявления'}, max_length=50, validators=[django.core.validators.RegexValidator(regex='^.{4,}$')], verbose_name='Товар'),
        ),
    ]