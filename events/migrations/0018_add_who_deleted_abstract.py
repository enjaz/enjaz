# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0017_add_teams'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='who_deleted',
            field=models.OneToOneField(related_name='deleted_abstracts', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
