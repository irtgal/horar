# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2020-10-06 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0005_auto_20201006_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='finnished',
            field=models.BooleanField(default=False),
        ),
    ]