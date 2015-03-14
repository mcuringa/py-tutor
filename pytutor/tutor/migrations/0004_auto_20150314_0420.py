# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0003_solution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendconnect',
            name='friend',
        ),
        migrations.DeleteModel(
            name='FriendConnect',
        ),
        migrations.RemoveField(
            model_name='message',
            name='msg_from',
        ),
        migrations.RemoveField(
            model_name='message',
            name='msg_to',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
