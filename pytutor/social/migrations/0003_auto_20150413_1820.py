# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20150413_0957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='friend_b',
            new_name='invited',
        ),
        migrations.RenameField(
            model_name='friendrequest',
            old_name='friend_a',
            new_name='sender',
        ),
    ]
