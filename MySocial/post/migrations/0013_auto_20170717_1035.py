# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 03:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_auto_20170717_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 3, 35, 34, 632000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 3, 35, 34, 631000, tzinfo=utc)),
        ),
    ]