# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_reorganize_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='secondary_clubs',
            field=models.ManyToManyField(related_name='secondary_activity', verbose_name='\u0627\u0644\u0623\u0646\u062f\u064a\u0629 \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0629', to='clubs.Club', blank=True),
        ),
    ]
