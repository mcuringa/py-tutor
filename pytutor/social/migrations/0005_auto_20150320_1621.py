# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20150318_0623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendconnection',
            name='accepted',
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 20, 16, 21, 27, 579827, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 3, 20, 16, 21, 36, 704765, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='muted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 20, 16, 21, 46, 400409, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 3, 20, 16, 21, 57, 200540, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='bio',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='city',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='country',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='first_name',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='institution',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='last_name',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='state',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
    ]
