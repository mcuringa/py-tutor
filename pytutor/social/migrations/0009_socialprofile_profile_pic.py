# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='profile_pic',
            field=models.ImageField(default=None, upload_to='profile_pics'),
            preserve_default=False,
        ),
    ]
