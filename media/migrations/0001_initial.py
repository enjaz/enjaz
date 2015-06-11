# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author_photo', models.ImageField(upload_to=b'media/author_photos/', verbose_name='\u0635\u0648\u0631\u0629 \u0634\u062e\u0635\u064a\u0629')),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0631\u0641\u0639')),
                ('title', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('text', models.TextField(null=True, verbose_name='\u0627\u0644\u0646\u0635', blank=True)),
                ('attachment', models.FileField(upload_to=b'media/articles/', null=True, verbose_name='\u0627\u0644\u0645\u0631\u0641\u0642\u0627\u062a', blank=True)),
                ('status', models.CharField(default=b'P', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(b'A', '\u062a\u0645 \u0642\u0628\u0648\u0644\u0647'), (b'P', '\u064a\u0646\u062a\u0638\u0631 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629'), (b'E', '\u064a\u0646\u062a\u0638\u0631 \u062a\u0639\u062f\u064a\u0644\u064b\u0627'), (b'R', '\u0645\u0631\u0641\u0648\u0636')])),
                ('assignee', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0643\u0644\u0641 \u0628\u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('author', models.ForeignKey(related_name='authored_articles', verbose_name='\u0627\u0644\u0643\u0627\u062a\u0628', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0642\u0627\u0644',
                'verbose_name_plural': '\u0627\u0644\u0645\u0642\u0627\u0644\u0627\u062a',
                'permissions': (('view_article', 'Can view all available articles.'), ('review_article', 'Can review any available article.')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_reviewed', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629')),
                ('notes', models.TextField(verbose_name='\u0627\u0644\u0645\u0644\u0627\u062d\u0638\u0627\u062a')),
                ('approve', models.BooleanField(default=False)),
                ('article', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0642\u0627\u0644', to='media.Article')),
                ('reviewer', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u064f\u0631\u0627\u062c\u0639', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0631\u0627\u062c\u0639\u0629 \u0645\u0642\u0627\u0644',
                'verbose_name_plural': '\u0645\u0631\u0627\u062c\u0639\u0627\u062a \u0627\u0644\u0645\u0642\u0627\u0644\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_assigned', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd8\xaa\xd8\xa7\xd8\xb1\xd9\x8a\xd8\xae \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb9\xd9\x8a\xd9\x8a\xd9\x86')),
                ('completed', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=140, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('description', models.TextField(null=True, verbose_name='\u0627\u0644\u0648\u0635\u0641', blank=True)),
                ('due_date', models.DateField(null=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0637\u0644\u0648\u0628', blank=True)),
                ('completed_date', models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0646\u0647\u0627\u0621', blank=True)),
                ('assignee', models.ForeignKey(related_name='assigned_tasks', verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb9\xd9\x8a\xd9\x91\xd9\x8e\xd9\x86', to=settings.AUTH_USER_MODEL)),
                ('assigner', models.ForeignKey(verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb9\xd9\x8a\xd9\x91\xd9\x90\xd9\x86', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0647\u0645\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u0647\u0627\u0645',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowUpReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0631\u0641\u0639 \u0627\u0644\u062a\u0642\u0631\u064a\u0631')),
                ('description', models.TextField(verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('start_date', models.DateField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('end_date', models.DateField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0647\u0627\u064a\u0629')),
                ('start_time', models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('end_time', models.TimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0646\u0647\u0627\u064a\u0629')),
                ('location', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646')),
                ('organizer_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646')),
                ('participant_count', models.IntegerField(verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646')),
                ('announcement_sites', models.TextField(verbose_name='\u0623\u0645\u0627\u0643\u0646 \u0627\u0644\u0646\u0634\u0631 \u0648 \u0627\u0644\u0625\u0639\u0644\u0627\u0646')),
                ('notes', models.TextField(null=True, verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a', blank=True)),
                ('episode', models.OneToOneField(verbose_name='\u0627\u0644\u0645\u0648\u0639\u062f', to='activities.Episode')),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u062a\u0642\u0631\u064a\u0631',
                'verbose_name_plural': '\u0627\u0644\u062a\u0642\u0627\u0631\u064a\u0631',
                'permissions': (('view_followupreport', 'Can view a follow-up report.'), ('view_all_followupreports', 'Can view all available follow-up reports.')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowUpReportImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.FileField(upload_to=b'media/images/', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629')),
                ('report', models.ForeignKey(related_name='images', to='media.FollowUpReport')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poll_type', models.IntegerField(verbose_name='\u0627\u0644\u0646\u0648\u0639', choices=[(0, '\u0645\u0627\u0630\u0627 \u0644\u0648\u061f'), (1, '\u0627\u0644\u0645\u0626\u0629 \u062a\u0642\u0648\u0644')])),
                ('title', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(null=True, upload_to=b'media/pollimages/', blank=True)),
                ('open_date', models.DateTimeField(verbose_name='\u0645\u0648\u0639\u062f \u0627\u0644\u0641\u062a\u062d')),
                ('close_date', models.DateTimeField(verbose_name='\u0645\u0648\u0639\u062f \u0627\u0644\u0625\u063a\u0644\u0627\u0642')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u062a\u0635\u0648\u064a\u062a',
                'verbose_name_plural': '\u0627\u0644\u062a\u0635\u0648\u064a\u062a\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0646\u0635')),
                ('color', models.CharField(default=b'green', max_length=128, verbose_name='\u0627\u0644\u0644\u0648\u0646', choices=[(b'red', '\u0623\u062d\u0645\u0631'), (b'green', '\u0623\u062e\u0636\u0631'), (b'blue', '\u0623\u0632\u0631\u0642'), (b'aero', '\u0631\u0635\u0627\u0635\u064a'), (b'grey', '\u0631\u0645\u0627\u062f\u064a'), (b'orange', '\u0628\u0631\u062a\u0642\u0627\u0644\u064a'), (b'yellow', '\u0623\u0635\u0641\u0631'), (b'pink', '\u0632\u0647\u0631\u064a'), (b'purple', '\u0628\u0646\u0641\u0633\u062c\u064a')])),
                ('poll', models.ForeignKey(related_name='choices', to='media.Poll')),
            ],
            options={
                'verbose_name': '\u062e\u064a\u0627\u0631',
                'verbose_name_plural': '\u0627\u0644\u062e\u064a\u0627\u0631\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u0646\u0635', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('poll', models.ForeignKey(related_name='comments', to='media.Poll')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PollResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(to='media.PollChoice')),
                ('poll', models.ForeignKey(related_name='responses', to='media.Poll')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u0646\u0635', blank=True)),
                ('author', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0639\u0644\u0651\u0650\u0642', to=settings.AUTH_USER_MODEL)),
                ('report', models.ForeignKey(related_name='comments', to='media.FollowUpReport')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0631\u0641\u0639 \u0627\u0644\u062a\u063a\u0637\u064a\u0629')),
                ('title', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('episode', models.OneToOneField(verbose_name='\u0627\u0644\u0645\u0648\u0639\u062f', to='activities.Episode')),
                ('writer', models.ForeignKey(verbose_name='\u0627\u0644\u0643\u0627\u062a\u0628', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u062a\u063a\u0637\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u062a\u063a\u0637\u064a\u0627\u062a',
                'permissions': (('view_story', 'Can view all available stories.'), ('edit_story', 'Can edit any available story.'), ('review_story', 'Can review any available story.'), ('assign_review_story', 'Can assign members to review stories.')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_reviewed', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629')),
                ('notes', models.TextField(verbose_name='\u0627\u0644\u0645\u0644\u0627\u062d\u0638\u0627\u062a')),
                ('approve', models.BooleanField(default=False)),
                ('reviewer', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u064f\u0631\u0627\u062c\u0639', to=settings.AUTH_USER_MODEL)),
                ('story', models.OneToOneField(verbose_name='\u0627\u0644\u062a\u063a\u0637\u064a\u0629', to='media.Story')),
            ],
            options={
                'verbose_name': '\u0645\u0631\u0627\u062c\u0639\u0629 \u062a\u063a\u0637\u064a\u0629',
                'verbose_name_plural': '\u0645\u0631\u0627\u062c\u0639\u0627\u062a \u0627\u0644\u062a\u063a\u0637\u064a\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoryTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_assigned', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd8\xaa\xd8\xa7\xd8\xb1\xd9\x8a\xd8\xae \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb9\xd9\x8a\xd9\x8a\xd9\x86')),
                ('completed', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(related_name='assigned_storytasks', verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb9\xd9\x8a\xd9\x91\xd9\x8e\xd9\x86', to=settings.AUTH_USER_MODEL)),
                ('assigner', models.ForeignKey(verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb9\xd9\x8a\xd9\x91\xd9\x90\xd9\x86', to=settings.AUTH_USER_MODEL)),
                ('episode', models.OneToOneField(to='activities.Episode')),
                ('story', models.OneToOneField(null=True, blank=True, to='media.Story')),
            ],
            options={
                'verbose_name': '\u0645\u0647\u0645\u0629 \u062a\u063a\u0637\u064a\u0629',
                'verbose_name_plural': '\u0645\u0647\u0645\u0627\u062a \u0627\u0644\u062a\u063a\u0637\u064a\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u0627\u0644\u062a\u0627\u0631\u064a\u062e')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u0646\u0635', blank=True)),
                ('author', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0639\u0644\u0642', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0647\u0645\u0629', to='media.CustomTask')),
            ],
            options={
                'verbose_name': '\u062a\u0639\u0644\u064a\u0642 \u0639\u0644\u0649 \u0645\u0647\u0645\u0629',
                'verbose_name_plural': '\u0627\u0644\u062a\u0639\u0644\u064a\u0642\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0645\u0647\u0627\u0645',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pollresponse',
            unique_together=set([('poll', 'user')]),
        ),
    ]
