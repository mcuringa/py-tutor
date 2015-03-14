# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.CharField(blank=True, max_length=20)),
                ('sent', models.DateTimeField(auto_now=True)),
                ('accepted', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('msg', models.TextField()),
                ('sent', models.DateTimeField(auto_now=True)),
                ('unread', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=120)),
                ('last_name', models.CharField(blank=True, max_length=120)),
                ('bio', models.CharField(blank=True, max_length=400)),
                ('public', models.BooleanField(default=False)),
                ('institution', models.CharField(blank=True, max_length=120)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('state', models.CharField(blank=True, max_length=120)),
                ('country', models.CharField(blank=True, max_length=120)),
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='msg_from',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='from_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='msg_to',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='to_user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='friend_a',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='frienda'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='friend_b',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='friendb'),
            preserve_default=True,
        ),
    ]
