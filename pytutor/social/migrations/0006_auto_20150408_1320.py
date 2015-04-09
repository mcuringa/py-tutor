# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20150320_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='socialprofile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='facebook',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='google',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='mobile',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='pyanywhere',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='skype',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='twitter',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='whatsapp',
            field=models.CharField(null=True, max_length=120, blank=True),
            preserve_default=True,
        ),
    ]
