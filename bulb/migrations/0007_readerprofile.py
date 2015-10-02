# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0006_online_sessions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReaderProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favorite_books', models.TextField(help_text='\u0645\u0646 \u0623\u0641\u0636\u0644 \u0627\u0644\u0643\u062a\u0628 \u0627\u0644\u062a\u064a \u0642\u0631\u0623\u062a\u060c \u0627\u062e\u062a\u0631 \u062b\u0644\u0627\u062b\u0629!', verbose_name='\u0643\u062a\u0628\u0643 \u0627\u0644\u0645\u0641\u0636\u0651\u0644\u0629.')),
                ('favorite_writers', models.TextField(help_text='\u0645\u0646 \u0623\u0641\u0636\u0644 \u0627\u0644\u0630\u064a\u0646 \u0642\u0631\u0623\u062a \u0644\u0647\u0645\u060c \u0627\u062e\u062a\u0631 \u062b\u0644\u0627\u062b\u0629!', verbose_name='\u0643\u064f\u062a\u0627\u0628\u0643 \u0648\u0643\u0627\u062a\u0628\u0627\u062a\u0643 \u0627\u0644\u0645\u0641\u0636\u0644\u064a\u0646')),
                ('areas_of_interests', models.TextField(help_text='\u0641\u064a\u0645 \u062a\u0641\u0636\u0644 \u0627\u0644\u0642\u0631\u0627\u0621\u0629\u061f', verbose_name='\u0645\u062c\u0627\u0644\u0627\u062a \u0627\u0647\u062a\u0645\u0627\u0645\u0643')),
                ('average_reading', models.CharField(help_text='\u0643\u0645 \u0643\u062a\u0627\u0628\u0627 \u062a\u0642\u0631\u0623 \u0641\u064a \u0627\u0644\u0633\u0646\u0629\u061f', max_length=200, verbose_name='\u0645\u0639\u062f\u0644 \u0627\u0644\u0642\u0631\u0627\u0621\u0629')),
                ('goodreads', models.CharField(help_text='\u0647\u0644 \u0644\u062f\u064a\u0643 \u062d\u0633\u0627\u0628 \u0639\u0644\u0649 \u0645\u0648\u0642\u0639 Goodreads\u061f (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', max_length=200, verbose_name='\u062d\u0633\u0627\u0628 Goodreads\u061f', blank=True)),
                ('twitter', models.CharField(help_text='\u0647\u0644 \u0644\u062f\u064a\u0643 \u062d\u0633\u0627\u0628 \u0639\u0644\u0649 \u062a\u0648\u064a\u062a\u0631\u061f (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', max_length=200, verbose_name='\u062d\u0633\u0627\u0628 \u062a\u0648\u064a\u062a\u0631\u061f', blank=True)),
                ('user', models.OneToOneField(related_name='reader_profile', verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
