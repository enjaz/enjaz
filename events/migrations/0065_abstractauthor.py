# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0064_choices'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of authors')),
                ('abstract', models.ForeignKey(related_name='author', to='events.Abstract')),
            ],
        ),
    ]
