# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0031_fill_can_view_assessments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buzz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u0646\u0635', blank=True)),
                ('title', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('announcement_date', models.DateTimeField(verbose_name='\u0648\u0642\u062a \u0627\u0644\u0625\u0639\u0644\u0627\u0646')),
                ('is_deleted', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to=b'media/buzzimages/', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629', blank=True)),
                ('colleges', models.ManyToManyField(to='clubs.College', verbose_name='\u0627\u0644\u0643\u0644\u064a\u0627\u062a \u0627\u0644\u0645\u0633\u062a\u0647\u062f\u0641\u0629', blank=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BuzzView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('on_date', models.DateTimeField(auto_now_add=True, verbose_name='\u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('off_date', models.DateTimeField(null=True, verbose_name='\u0627\u0644\u0646\u0647\u0627\u064a\u0629', blank=True)),
                ('buzz', models.ForeignKey(to='media.Buzz')),
                ('viewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
