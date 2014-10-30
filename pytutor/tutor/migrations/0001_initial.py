# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveQuestion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('function_name', models.CharField(max_length=300)),
                ('prompt', models.TextField()),
                ('solution', models.TextField(blank=True)),
                ('level', models.IntegerField(default=1, choices=[(1, '1. Basics: simple function, variables, operators (e.g., +,-,*/)'), (2, '2. Conditional statements, built-in functions'), (3, '3. Strings, basics'), (4, '4. Lists and loops'), (5, '5. Dictionaries, tuples, sets; string functions'), (6, '6. Multi-step problems, libraries, OOP, etc'), (7, '7. Hard problems')])),
                ('tags', models.CharField(max_length=500, blank=True)),
                ('version', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=500, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('archived', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tutor_archivequestion_creator')),
                ('modifier', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tutor_archivequestion_modifer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FriendConnect',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=20, blank=True)),
                ('sent', models.DateTimeField(auto_now=True)),
                ('friend', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='friend')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('msg', models.TextField()),
                ('sent', models.DateTimeField(auto_now=True)),
                ('unread', models.BooleanField(default=True)),
                ('msg_from', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='from_user')),
                ('msg_to', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='to_user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('function_name', models.CharField(max_length=300)),
                ('prompt', models.TextField()),
                ('solution', models.TextField(blank=True)),
                ('level', models.IntegerField(default=1, choices=[(1, '1. Basics: simple function, variables, operators (e.g., +,-,*/)'), (2, '2. Conditional statements, built-in functions'), (3, '3. Strings, basics'), (4, '4. Lists and loops'), (5, '5. Dictionaries, tuples, sets; string functions'), (6, '6. Multi-step problems, libraries, OOP, etc'), (7, '7. Hard problems')])),
                ('tags', models.CharField(max_length=500, blank=True)),
                ('version', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=500, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=1)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tutor_question_creator')),
                ('modifier', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='tutor_question_modifer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionFlag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('flag', models.IntegerField(choices=[(1, 'Unclear'), (2, 'Too Hard for Level'), (3, 'Too Easy for Level'), (4, 'Innapropriate')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(to='tutor.ArchiveQuestion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('code', models.TextField(help_text='Your solution to this question.', blank=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('attempt', models.IntegerField(default=1)),
                ('submitted', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(to='tutor.Question')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('args', models.CharField(max_length=500, blank=True)),
                ('result', models.TextField()),
                ('question', models.ForeignKey(to='tutor.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('id', 'version')]),
        ),
        migrations.AddField(
            model_name='archivequestion',
            name='parent',
            field=models.ForeignKey(to='tutor.Question'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='archivequestion',
            unique_together=set([('parent', 'version')]),
        ),
    ]
