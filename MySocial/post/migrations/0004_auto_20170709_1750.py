# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 00:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 10, 0, 50, 5, 780000, tzinfo=utc)),
        ),
    ]
