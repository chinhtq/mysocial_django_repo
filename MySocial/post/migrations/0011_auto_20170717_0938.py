# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 02:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0010_auto_20170713_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 2, 38, 46, 957000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 17, 2, 38, 46, 956000, tzinfo=utc)),
        ),
    ]
