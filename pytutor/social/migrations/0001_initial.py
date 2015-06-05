# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutor', '0004_auto_20150314_0420'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=20, blank=True)),
                ('sent', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HelpRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(to='tutor.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('msg', models.TextField()),
                ('sent', models.DateTimeField(auto_now=True)),
                ('unread', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('bio', models.CharField(null=True, max_length=200, blank=True)),
                ('public', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(null=True, upload_to='profile_pics', blank=True)),
                ('institution', models.CharField(null=True, max_length=120, blank=True)),
                ('city', models.CharField(null=True, max_length=120, blank=True)),
                ('state', models.CharField(null=True, max_length=120, blank=True)),
                ('country', models.CharField(null=True, max_length=120, blank=True)),
                ('mobile', models.CharField(null=True, max_length=120, blank=True)),
                ('facebook', models.CharField(null=True, max_length=120, blank=True)),
                ('twitter', models.CharField(null=True, max_length=120, blank=True)),
                ('whatsapp', models.CharField(null=True, max_length=120, blank=True)),
                ('skype', models.CharField(null=True, max_length=120, blank=True)),
                ('google', models.CharField(null=True, max_length=120, blank=True)),
                ('pyanywhere', models.CharField(null=True, max_length=120, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='msg_from',
            field=models.ForeignKey(related_name='from_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='msg_to',
            field=models.ForeignKey(related_name='to_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='helprequest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='invited',
            field=models.ForeignKey(related_name='invited', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='sender',
            field=models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='friend_a',
            field=models.ForeignKey(related_name='frienda', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='friend_b',
            field=models.ForeignKey(related_name='friendb', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RestProfile',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('social.socialprofile',),
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
    ]
