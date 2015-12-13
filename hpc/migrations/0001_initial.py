# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Abstract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name=b'Title')),
                ('authors', models.TextField(verbose_name='Name of authors')),
                ('university', models.CharField(max_length=128, verbose_name=b'University')),
                ('college', models.CharField(max_length=128, verbose_name=b'College')),
                ('presenting_author', models.CharField(max_length=128, verbose_name=b'Presenting author')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('phone', models.CharField(max_length=128, verbose_name=b'Phone number')),
                ('presentation_preference', models.CharField(max_length=128, verbose_name=b'Presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')])),
                ('attachment', models.FileField(upload_to=b'hpc/abstract/', verbose_name='Attach the abstract')),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
