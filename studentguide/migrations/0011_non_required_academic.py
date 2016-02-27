# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0010_create_mentor_of_the_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideprofile',
            name='nonacademic_interests',
            field=models.TextField(help_text='\u0628\u0639\u064a\u062f\u0627 \u0639\u0646 \u0627\u0644\u062a\u062d\u0635\u064a\u0644 \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u060c \u0645\u0627 \u0627\u0644\u0630\u064a \u064a\u0634\u063a\u0644\u0643\u061f', verbose_name='\u0627\u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0627\u062a \u063a\u064a\u0631  \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u0629', blank=True),
        ),
    ]
