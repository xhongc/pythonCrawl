# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-22 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='money',
            field=models.CharField(max_length=30, null=True, verbose_name='金额'),
        ),
        migrations.AlterField(
            model_name='people',
            name='username',
            field=models.CharField(max_length=30, null=True, verbose_name='姓名'),
        ),
    ]
