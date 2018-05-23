# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-22 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=30, null=True, verbose_name='姓名')),
                ('money', models.CharField(blank=True, max_length=30, null=True, verbose_name='金额')),
            ],
        ),
    ]
