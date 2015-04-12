# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_auto_20150410_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pics', blank=True, null=True),
            preserve_default=True,
        ),
    ]
