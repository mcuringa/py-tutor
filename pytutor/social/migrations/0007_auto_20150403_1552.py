# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_auto_20150403_1539'),
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
    ]
