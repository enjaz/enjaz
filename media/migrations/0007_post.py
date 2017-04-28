# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0006_change_story_arabic_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('slug', models.SlugField(verbose_name='\u0627\u0644\u0631\u0627\u0628\u0637')),
                ('body', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('announcement_date', models.DateTimeField(null=True, verbose_name='\u0648\u0642\u062a \u0627\u0644\u0625\u0639\u0644\u0627\u0646', blank=True)),
                ('image', models.ImageField(upload_to=b'media/post/', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629', blank=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
