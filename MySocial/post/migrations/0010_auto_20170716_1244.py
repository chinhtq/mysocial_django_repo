# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 19:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20170716_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 16, 19, 44, 7, 760000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 16, 19, 44, 7, 759000, tzinfo=utc)),
        ),
    ]