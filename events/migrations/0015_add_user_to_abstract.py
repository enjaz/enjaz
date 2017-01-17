# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0014_expand_abstract_submission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstract',
            name='conclusion',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='discussion',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='methodology',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='results',
        ),
        migrations.AddField(
            model_name='abstract',
            name='user',
            field=models.ForeignKey(related_name='event_Abstract', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
