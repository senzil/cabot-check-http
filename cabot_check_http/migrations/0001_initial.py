# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-13 11:44
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cabotapp', '0006_auto_20170821_1000'),
    ]

    operations = [
            migrations.CreateModel(
            name='HttpStatusCheck',
            fields=[
            ],
            options={
                'abstract': False,
                'proxy': True,
            },
            bases=('cabotapp.statuscheck',),
        ),
       
    ]



