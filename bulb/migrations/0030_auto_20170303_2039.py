# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0029_null_previoys_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='culturalproduct',
            name='readathon',
        ),
        migrations.RemoveField(
            model_name='debate',
            name='invitation',
        ),
        migrations.RemoveField(
            model_name='debatecomment',
            name='debate',
        ),
        migrations.RemoveField(
            model_name='debatecomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='CulturalProduct',
        ),
        migrations.DeleteModel(
            name='Debate',
        ),
        migrations.DeleteModel(
            name='DebateComment',
        ),
    ]
