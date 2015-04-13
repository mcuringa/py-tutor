# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0001_squashed_0013_socialprofile_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=20)),
                ('sent', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('friend_a', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('friend_b', models.ForeignKey(related_name='invited', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicRestProfile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('social.restprofile',),
        ),
        migrations.RemoveField(
            model_name='friendconnection',
            name='created',
        ),
        migrations.RemoveField(
            model_name='friendconnection',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='friendconnection',
            name='muted',
        ),
        migrations.RemoveField(
            model_name='friendconnection',
            name='sent',
        ),
        migrations.RemoveField(
            model_name='friendconnection',
            name='status',
        ),
    ]
