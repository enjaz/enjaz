# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('newhpc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.FileField(upload_to=b'newhpc/gallery/', null=True, verbose_name=b'Attach the picture', blank=True)),
                ('show_more', models.URLField(default=b'', verbose_name=b'Show more link')),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_top_speaker', models.BooleanField(default=False, verbose_name=b'\xd9\x87\xd9\x84 \xd9\x87\xd9\x88 \xd9\x85\xd9\x86 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd9\x91\xd8\xab\xd9\x8a\xd9\x86 \xd8\xa7\xd9\x84\xd8\xa8\xd8\xa7\xd8\xb1\xd8\xb2\xd9\x8a\xd9\x86 \xd8\xa7\xd9\x84\xd8\xb0\xd9\x8a\xd9\x86 \xd8\xb3\xd9\x8a\xd8\xaa\xd9\x85 \xd8\xb9\xd8\xb1\xd8\xb6\xd9\x87\xd9\x85 \xd9\x81\xd9\x8a \xd8\xa7\xd9\x84\xd8\xb5\xd9\x81\xd8\xad\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb1\xd8\xa6\xd9\x8a\xd8\xb3\xd9\x8a\xd9\x91\xd8\xa9')),
                ('name', models.CharField(default=b'', max_length=255, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd9\x91\xd8\xab \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd9\x88\xd9\x81\xd9\x91\xd8\xb1\xd8\xa9', blank=True)),
                ('position', models.CharField(default=b'', max_length=255, verbose_name=b'\xd9\x85\xd9\x86\xd8\xb5\xd8\xa8 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd9\x91\xd8\xab \xd9\x85\xd8\xb7\xd9\x84\xd9\x88\xd8\xa8 \xd9\x81\xd9\x8a \xd8\xad\xd8\xa7\xd9\x84 \xd9\x83\xd8\xa7\xd9\x86 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd9\x91\xd8\xab \xd8\xa8\xd8\xa7\xd8\xb1\xd8\xb2', blank=True)),
                ('image', models.ImageField(upload_to=b'newhpc/previous/speaker', null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb5\xd9\x88\xd8\xb1\xd8\xa9 \xd9\x85\xd8\xb7\xd9\x84\xd9\x88\xd8\xa8\xd8\xa9 \xd9\x81\xd9\x8a \xd8\xad\xd8\xa7\xd9\x84 \xd9\x83\xd9\x88\xd9\x86 \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd9\x91\xd8\xab \xd8\xa8\xd8\xa7\xd8\xb1\xd8\xb2', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mediasponser',
            name='version',
        ),
        migrations.RemoveField(
            model_name='hpcleader',
            name='english_name',
        ),
        migrations.RemoveField(
            model_name='previousstatistics',
            name='arabic_name',
        ),
        migrations.RemoveField(
            model_name='previousstatistics',
            name='english_name',
        ),
        migrations.RemoveField(
            model_name='previousstatistics',
            name='number_of_attendee',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='arabic_description',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='english_description',
        ),
        migrations.RemoveField(
            model_name='winner',
            name='english_name',
        ),
        migrations.AddField(
            model_name='previousstatistics',
            name='number_of_lectures',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xa7\xd9\x84\xd9\x85\xd8\xad\xd8\xa7\xd8\xb6\xd8\xb1\xd8\xa7\xd8\xaa'),
        ),
        migrations.AddField(
            model_name='previousstatistics',
            name='number_of_winners',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xa7\xd9\x84\xd9\x81\xd8\xa7\xd8\xa6\xd8\xb2\xd9\x8a\xd9\x86 \xd8\xa8\xd8\xa7\xd9\x84\xd8\xa3\xd8\xa8\xd8\xad\xd8\xa7\xd8\xab'),
        ),
        migrations.AddField(
            model_name='previousstatistics',
            name='oral_presentations',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd9\x88\xd8\xb6 \xd8\xa7\xd9\x84\xd8\xa8\xd8\xad\xd8\xab\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AddField(
            model_name='previousstatistics',
            name='poster_presentations',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd9\x84\xd8\xb5\xd9\x82\xd8\xa7\xd8\xaa \xd8\xa7\xd9\x84\xd8\xa8\xd8\xad\xd8\xab\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AddField(
            model_name='previousversion',
            name='logo',
            field=models.ImageField(upload_to=b'newhpc/prevous/logo', null=True, verbose_name=b'\xd8\xb4\xd8\xb9\xd8\xa7\xd8\xb1 \xd8\xa7\xd9\x84\xd9\x86\xd8\xb3\xd8\xae\xd8\xa9', blank=True),
        ),
        migrations.AddField(
            model_name='winner',
            name='presentation_type',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'\xd9\x86\xd9\x88\xd8\xb9 \xd8\xa7\xd9\x84\xd8\xa8\xd8\xad\xd8\xab', choices=[(b'O', b'Oral'), (b'P', b'Poster')]),
        ),
        migrations.AddField(
            model_name='winner',
            name='rank',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2', choices=[(b'1', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xa3\xd9\x88\xd9\x91\xd9\x84'), (b'2', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xab\xd8\xa7\xd9\x86\xd9\x8a'), (b'3', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xab\xd8\xa7\xd9\x84\xd8\xab'), (b'4', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xb1\xd8\xa7\xd8\xa8\xd8\xb9'), (b'5', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xae\xd8\xa7\xd9\x85\xd8\xb3'), (b'6', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xb3\xd8\xa7\xd8\xaf\xd8\xb3'), (b'7', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xb3\xd8\xa7\xd8\xa8\xd8\xb9'), (b'8', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xab\xd8\xa7\xd9\x85\xd9\x86'), (b'9', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xaa\xd8\xa7\xd8\xb3\xd8\xb9'), (b'10', b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd9\x83\xd8\xb2 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xa7\xd8\xb4\xd8\xb1')]),
        ),
        migrations.AlterField(
            model_name='blogpostarabic',
            name='author',
            field=models.ForeignKey(related_name='arabic_post_author', default=b'', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blogpostarabic',
            name='image',
            field=models.ImageField(null=True, upload_to=b'newhpc/blog/arabic', blank=True),
        ),
        migrations.AlterField(
            model_name='blogpostarabic',
            name='summary',
            field=models.TextField(default=b'', verbose_name=b'240 character summary'),
        ),
        migrations.AlterField(
            model_name='blogpostarabic',
            name='text',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='blogpostarabic',
            name='title',
            field=models.CharField(default=b'', max_length=400),
        ),
        migrations.AlterField(
            model_name='blogpostenglish',
            name='image',
            field=models.ImageField(null=True, upload_to=b'newhpc/blog/english', blank=True),
        ),
        migrations.AlterField(
            model_name='blogpostenglish',
            name='summary',
            field=models.TextField(default=b'', verbose_name=b'240 character summary'),
        ),
        migrations.AlterField(
            model_name='blogpostenglish',
            name='text',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='blogpostenglish',
            name='title',
            field=models.CharField(default=b'', max_length=400),
        ),
        migrations.AlterField(
            model_name='faqcategory',
            name='arabic_title',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb5\xd9\x86\xd9\x8a\xd9\x81 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='faqcategory',
            name='english_title',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb5\xd9\x86\xd9\x8a\xd9\x81 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='faqquestion',
            name='arabic_answer',
            field=models.TextField(default=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xac\xd9\x88\xd8\xa7\xd8\xa8 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='faqquestion',
            name='arabic_question',
            field=models.TextField(default=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='faqquestion',
            name='english_answer',
            field=models.TextField(default=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xac\xd9\x88\xd8\xa7\xd8\xa8 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='faqquestion',
            name='english_question',
            field=models.TextField(default=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='hpcleader',
            name='arabic_name',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='hpcleader',
            name='image',
            field=models.ImageField(upload_to=b'newhpc/previous/HpcLeader', null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb5\xd9\x88\xd8\xb1\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb4\xd8\xae\xd8\xb5\xd9\x8a\xd9\x91\xd8\xa9', blank=True),
        ),
        migrations.AlterField(
            model_name='previousstatistics',
            name='number_of_abstracts',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xa7\xd9\x84\xd8\xa3\xd8\xa8\xd8\xad\xd8\xa7\xd8\xab \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd9\x82\xd8\xaf\xd9\x91\xd9\x85\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='previousstatistics',
            name='number_of_accepted_abstracts',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xa7\xd9\x84\xd8\xa3\xd8\xa8\xd8\xad\xd8\xa7\xd8\xab \xd8\xa7\xd9\x84\xd9\x85\xd9\x82\xd8\xa8\xd9\x88\xd9\x84\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='previousstatistics',
            name='number_of_signs',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xaa\xd8\xb3\xd8\xac\xd9\x8a\xd9\x84\xd8\xa7\xd8\xaa \xd8\xa7\xd9\x84\xd8\xaf\xd8\xae\xd9\x88\xd9\x84 \xd9\x88\xd8\xa7\xd9\x84\xd8\xae\xd8\xb1\xd9\x88\xd8\xac \xd8\xae\xd9\x84\xd8\xa7\xd9\x84 \xd8\xa3\xd9\x8a\xd9\x91\xd8\xa7\xd9\x85 \xd8\xa7\xd9\x84\xd9\x85\xd8\xa4\xd8\xaa\xd9\x85\xd8\xb1 \xd8\xa7\xd9\x84\xd8\xab\xd9\x84\xd8\xa7\xd8\xab'),
        ),
        migrations.AlterField(
            model_name='previousstatistics',
            name='number_of_speakers',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xa7\xd9\x84\xd9\x85\xd8\xaa\xd8\xad\xd8\xaf\xd9\x91\xd8\xab\xd9\x8a\xd9\x86'),
        ),
        migrations.AlterField(
            model_name='previousstatistics',
            name='number_of_universities',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd8\xa7\xd9\x84\xd8\xac\xd8\xa7\xd9\x85\xd8\xb9\xd8\xa7\xd8\xaa \xd8\xa7\xd9\x84\xd9\x85\xd8\xb4\xd8\xa7\xd8\xb1\xd9\x83\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='previousstatistics',
            name='number_of_workshops',
            field=models.IntegerField(default=0, verbose_name=b'\xd8\xb9\xd8\xaf\xd8\xaf \xd9\x88\xd8\xb1\xd8\xb4 \xd8\xa7\xd9\x84\xd8\xb9\xd9\x85\xd9\x84'),
        ),
        migrations.AlterField(
            model_name='previousversion',
            name='arabic_title',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd9\x86\xd8\xb3\xd8\xae\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='previousversion',
            name='arabic_vision',
            field=models.TextField(default=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb1\xd8\xa4\xd9\x8a\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9 \xd8\xba\xd9\x8a\xd8\xb1 \xd9\x85\xd8\xb7\xd9\x84\xd9\x88\xd8\xa8', blank=True),
        ),
        migrations.AlterField(
            model_name='previousversion',
            name='english_title',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa7\xd9\x84\xd9\x86\xd8\xb3\xd8\xae\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='previousversion',
            name='english_vision',
            field=models.TextField(default=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb1\xd8\xa4\xd9\x8a\xd8\xa9 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xa7\xd9\x86\xd8\xac\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd9\x91\xd8\xa9 \xd8\xba\xd9\x8a\xd8\xb1 \xd9\x85\xd8\xb7\xd9\x84\xd9\x88\xd8\xa8', blank=True),
        ),
        migrations.AlterField(
            model_name='winner',
            name='arabic_name',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xa7\xd8\xb3\xd9\x85 \xd8\xa8\xd8\xa7\xd9\x84\xd9\x84\xd8\xba\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb9\xd8\xb1\xd8\xa8\xd9\x8a\xd9\x91\xd8\xa9'),
        ),
        migrations.AlterField(
            model_name='winner',
            name='image',
            field=models.ImageField(upload_to=b'newhpc/previous/winner/', null=True, verbose_name=b'\xd8\xb5\xd9\x88\xd8\xb1\xd8\xa9 \xd8\xa7\xd9\x84\xd9\x81\xd8\xa7\xd8\xa6\xd8\xb2 \xd8\xba\xd9\x8a\xd8\xb1 \xd9\x85\xd8\xb7\xd9\x84\xd9\x88\xd8\xa8\xd8\xa9 \xd9\x81\xd9\x8a \xd8\xad\xd8\xa7\xd9\x84 \xd8\xb9\xd8\xaf\xd9\x85 \xd8\xa7\xd9\x84\xd8\xaa\xd9\x88\xd9\x81\xd9\x91\xd8\xb1', blank=True),
        ),
        migrations.DeleteModel(
            name='MediaSponser',
        ),
        migrations.AddField(
            model_name='speaker',
            name='version',
            field=models.ForeignKey(to='newhpc.PreviousVersion'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='version',
            field=models.ForeignKey(to='newhpc.PreviousVersion'),
        ),
    ]
