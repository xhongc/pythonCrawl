# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-06 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wxsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wx_session', models.CharField(blank=True, max_length=65, null=True, verbose_name='wx_session')),
            ],
            options={
                'verbose_name': '微信授权',
                'verbose_name_plural': '微信授权',
            },
        ),
    ]
