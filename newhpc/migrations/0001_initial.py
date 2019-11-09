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
            name='BlogPostArabic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=400)),
                ('summary', models.TextField(verbose_name=b'240 character summary')),
                ('text', models.TextField()),
                ('image', models.ImageField(null=True, upload_to=b'hpc/blog/arabic', blank=True)),
                ('author', models.ForeignKey(related_name='arabic_post_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPostEnglish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=400)),
                ('summary', models.TextField(verbose_name=b'240 character summary')),
                ('text', models.TextField()),
                ('image', models.ImageField(null=True, upload_to=b'hpc/blog/english', blank=True)),
                ('author', models.ForeignKey(related_name='english_post_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arabic_title', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb5\xd9\x86\xd9\x8a\xd9\x81 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9')),
                ('english_title', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb5\xd9\x86\xd9\x8a\xd9\x81 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9')),
            ],
        ),
        migrations.CreateModel(
            name='FaqQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_tech', models.BooleanField(default=False, verbose_name=b'\xd9\x87\xd9\x84 \xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84 \xd8\xaa\xd9\x82\xd9\x86\xd9\x8a \xd8\x9f')),
                ('arabic_question', models.TextField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9')),
                ('english_question', models.TextField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9')),
                ('arabic_answer', models.TextField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xac\xd9\x88\xd8\xa7\xd8\xa8 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9')),
                ('english_answer', models.TextField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xac\xd9\x88\xd8\xa7\xd8\xa8 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9')),
                ('category', models.ForeignKey(related_name='faq_category', verbose_name=b'\xd8\xa7\xd8\xae\xd8\xaa\xd8\xb1 \xd8\xaa\xd8\xb5\xd9\x86\xd9\x8a\xd9\x81 \xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84', to='newhpc.FaqCategory')),
            ],
        ),
        migrations.CreateModel(
            name='HpcLeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arabic_name', models.CharField(max_length=255, null=True)),
                ('english_name', models.CharField(max_length=255, null=True)),
                ('image', models.ImageField(null=True, upload_to=b'hpc/previous/HpcLeader', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaSponser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arabic_name', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9')),
                ('english_name', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9')),
                ('logo', models.ImageField(null=True, upload_to=b'hpc/previous/media', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PreviousStatistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arabic_name', models.CharField(max_length=255, null=True)),
                ('english_name', models.CharField(max_length=255, null=True)),
                ('number_of_attendee', models.IntegerField()),
                ('number_of_workshops', models.IntegerField()),
                ('number_of_speakers', models.IntegerField()),
                ('number_of_abstracts', models.IntegerField()),
                ('number_of_accepted_abstracts', models.IntegerField()),
                ('number_of_universities', models.IntegerField()),
                ('number_of_signs', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PreviousVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arabic_title', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd9\x86\xd8\xb3\xd8\xae\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9')),
                ('english_title', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd9\x86\xd8\xb3\xd8\xae\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9')),
                ('arabic_vision', models.TextField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb1\xd8\xa4\xd9\x8a\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9', blank=True)),
                ('english_vision', models.TextField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb1\xd8\xa4\xd9\x8a\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arabic_name', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9')),
                ('english_name', models.CharField(max_length=255, null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9')),
                ('arabic_description', models.TextField(null=True)),
                ('english_description', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to=b'hpc/previous/winner/', blank=True)),
                ('version', models.ForeignKey(to='newhpc.PreviousVersion')),
            ],
        ),
        migrations.AddField(
            model_name='previousstatistics',
            name='version',
            field=models.ForeignKey(to='newhpc.PreviousVersion'),
        ),
        migrations.AddField(
            model_name='mediasponser',
            name='version',
            field=models.ForeignKey(to='newhpc.PreviousVersion'),
        ),
        migrations.AddField(
            model_name='hpcleader',
            name='version',
            field=models.ForeignKey(to='newhpc.PreviousVersion'),
        ),
    ]
