# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_divide_abstract_again'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='study_field',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Field'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='user',
            field=models.ForeignKey(related_name='event_abstracts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
