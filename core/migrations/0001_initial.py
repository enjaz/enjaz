# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0646\u0648\u0639', choices=[(b'R', '\u0625\u0639\u0644\u0627\u0646 \u0628\u062d\u062b'), (b'E', '\u0625\u0639\u0644\u0627\u0646 \u062c\u0647\u0629 \u062e\u0627\u0631\u062c\u064a\u0629'), (b'M', '\u0625\u0639\u0644\u0627\u0646 \u0628\u0631\u0646\u0627\u0645\u062c \u0639\u0627\u0645 \u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628')])),
                ('title', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('description', models.TextField(verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('image', models.ImageField(null=True, upload_to=b'announcement_images', blank=True)),
                ('url', models.URLField(verbose_name='\u0627\u0644\u0631\u0627\u0628\u0637')),
                ('visits', models.PositiveIntegerField(default=0, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0632\u064a\u0627\u0631\u0627\u062a')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0646\u0634\u0627\u0621')),
            ],
            options={
                'verbose_name': '\u0625\u0639\u0644\u0627\u0646',
                'verbose_name_plural': '\u0627\u0644\u0625\u0639\u0644\u0627\u0646\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'sc-publications/', verbose_name='\u0627\u0644\u0645\u0644\u0641')),
                ('label', models.CharField(max_length=128, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0636\u0627\u0641\u0629')),
            ],
            options={
                'verbose_name': '\u0625\u0635\u062f\u0627\u0631',
                'verbose_name_plural': '\u0627\u0644\u0625\u0635\u062f\u0627\u0631\u0627\u062a',
            },
            bases=(models.Model,),
        ),
    ]
