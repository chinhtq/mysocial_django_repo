# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20170716_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name'], 'permissions': (('can_post', 'Can post in group'),)},
        ),
    ]