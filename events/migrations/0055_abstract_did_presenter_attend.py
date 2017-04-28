# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0054_question_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='did_presenter_attend',
            field=models.BooleanField(default=False, verbose_name='\u062d\u0636\u0631 \u0627\u0644\u0645\u0642\u062f\u0645\u061f'),
        ),
    ]
