# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_job_description_textarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonprofile',
            name='alternative_email',
            field=models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a  \u0627\u0644\u0634\u062e\u0635\u064a \u0627\u0644\u0628\u062f\u064a\u0644', blank=True),
        ),
    ]
