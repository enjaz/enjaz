# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0061_surveyquestion_is_english'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyquestion',
            name='text',
            field=models.TextField(verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644'),
        ),
    ]
