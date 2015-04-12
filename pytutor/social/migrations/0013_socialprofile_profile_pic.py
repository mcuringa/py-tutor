# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0012_remove_socialprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialprofile',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pics', null=True, blank=True),
        ),
    ]
