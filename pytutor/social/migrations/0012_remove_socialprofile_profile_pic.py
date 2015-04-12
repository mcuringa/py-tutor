# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0011_auto_20150410_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialprofile',
            name='profile_pic',
        ),
    ]
