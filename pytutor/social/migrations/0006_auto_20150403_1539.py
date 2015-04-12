# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0005_auto_20150320_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='facebook',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='google',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='mobile',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='pyanywhere',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='skype',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='twitter',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='whatsapp',
            field=models.CharField(blank=True, null=True, max_length=120),
            preserve_default=True,
        ),
    ]
