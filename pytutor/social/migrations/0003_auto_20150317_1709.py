# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_create_profiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestProfile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('social.socialprofile',),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='bio',
            field=models.CharField(blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
