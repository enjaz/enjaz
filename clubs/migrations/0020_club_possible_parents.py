# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_club_can_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='possible_parents',
            field=models.ManyToManyField(related_name='possible_parents_rel_+', verbose_name='\u0627\u0644\u0646\u0648\u0627\u062f\u064a \u0627\u0644\u0623\u0628 \u0627\u0644\u0645\u0645\u0643\u0646\u0629', to='clubs.Club', blank=True),
        ),
    ]
