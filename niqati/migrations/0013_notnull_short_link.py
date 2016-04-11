# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0012_field_cleanup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='short_link',
            field=models.URLField(default=b'', verbose_name='\u0631\u0627\u0628\u0637 \u0642\u0635\u064a\u0631', blank=True),
        ),
    ]
