# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20150317_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='bio',
            field=models.CharField(null=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='city',
            field=models.CharField(null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='country',
            field=models.CharField(null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='first_name',
            field=models.CharField(null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='institution',
            field=models.CharField(null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='last_name',
            field=models.CharField(null=True, max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='state',
            field=models.CharField(null=True, max_length=120),
            preserve_default=True,
        ),
    ]
