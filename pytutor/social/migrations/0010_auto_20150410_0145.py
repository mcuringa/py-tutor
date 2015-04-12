# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_socialprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='profile_pics'),
            preserve_default=True,
        ),
    ]
