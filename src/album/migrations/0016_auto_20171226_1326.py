# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-26 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0015_auto_20171204_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
