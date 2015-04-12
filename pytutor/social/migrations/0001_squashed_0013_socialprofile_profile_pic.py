# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# social.migrations.0002_create_profiles

class Migration(migrations.Migration):

    replaces = [('social', '0001_initial'), ('social', '0002_create_profiles'), ('social', '0003_auto_20150317_1709'), ('social', '0004_auto_20150318_0623'), ('social', '0005_auto_20150320_1621'), ('social', '0006_auto_20150403_1539'), ('social', '0007_auto_20150403_1552'), ('social', '0006_auto_20150408_1320'), ('social', '0008_merge'), ('social', '0009_socialprofile_profile_pic'), ('social', '0010_auto_20150410_0145'), ('social', '0011_auto_20150410_0146'), ('social', '0012_remove_socialprofile_profile_pic'), ('social', '0013_socialprofile_profile_pic')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendConnection',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('status', models.CharField(blank=True, max_length=20)),
                ('sent', models.DateTimeField(auto_now=True)),
                ('accepted', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('msg', models.TextField()),
                ('sent', models.DateTimeField(auto_now=True)),
                ('unread', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SocialProfile',
            fields=[
                ('bio', models.CharField(blank=True, max_length=400)),
                ('public', models.BooleanField(default=False)),
                ('institution', models.CharField(blank=True, max_length=120)),
                ('city', models.CharField(blank=True, max_length=120)),
                ('state', models.CharField(blank=True, max_length=120)),
                ('country', models.CharField(blank=True, max_length=120)),
                ('user', models.OneToOneField(serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
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
            model_name='friendconnection',
            name='friend_a',
            field=models.ForeignKey(related_name='frienda', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='friend_b',
            field=models.ForeignKey(related_name='friendb', to=settings.AUTH_USER_MODEL),
        ),
        # migrations.RunPython(
        #     code=social.migrations.0002_create_profiles.Migration.create_profiles,
        # ),
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
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='bio',
            field=models.CharField(null=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='city',
            field=models.CharField(null=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='country',
            field=models.CharField(null=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='institution',
            field=models.CharField(null=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='state',
            field=models.CharField(null=True, max_length=120),
        ),
        migrations.RemoveField(
            model_name='friendconnection',
            name='accepted',
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 3, 20, 16, 21, 27, 579827, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 3, 20, 16, 21, 36, 704765, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='friendconnection',
            name='muted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 3, 20, 16, 21, 46, 400409, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 3, 20, 16, 21, 57, 200540, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='bio',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='city',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='country',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='institution',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='socialprofile',
            name='state',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='facebook',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='google',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='mobile',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='pyanywhere',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='skype',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='twitter',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='whatsapp',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='facebook',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='google',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='mobile',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='pyanywhere',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='skype',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='twitter',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='whatsapp',
            field=models.CharField(null=True, blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='socialprofile',
            name='profile_pic',
            field=models.ImageField(upload_to='profile_pics', null=True, blank=True),
        ),
    ]
