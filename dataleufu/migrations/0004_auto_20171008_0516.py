# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-08 05:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataleufu', '0003_auto_20171007_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dataleufu.UserGroup'),
        ),
    ]
