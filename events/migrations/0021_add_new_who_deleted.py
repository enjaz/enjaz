# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0020_add_field_to_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='who_deleted_abstract',
            field=models.ForeignKey(related_name='user_deleted_abstracts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
