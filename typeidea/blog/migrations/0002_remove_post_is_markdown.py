# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-09 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_markdown',
        ),
    ]