# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 07:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rateMyCourse', '0005_auto_20171030_2031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='C_scroe',
            new_name='C_score',
        ),
    ]