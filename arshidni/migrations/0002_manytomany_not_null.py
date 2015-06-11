# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('arshidni', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='members',
            field=models.ManyToManyField(related_name='studygroup_memberships', verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
