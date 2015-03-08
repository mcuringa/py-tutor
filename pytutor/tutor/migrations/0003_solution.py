# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0002_q_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tutor.archivequestion',),
        ),
    ]
