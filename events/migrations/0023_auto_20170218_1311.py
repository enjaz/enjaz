# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_abstract_evaluators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='abstract',
            field=models.ForeignKey(related_name='abstract_evaluation', to='events.Abstract'),
        ),
    ]
