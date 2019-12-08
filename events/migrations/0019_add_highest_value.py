# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_add_who_deleted_abstract'),
    ]

    operations = [
        migrations.AddField(
            model_name='criterion',
            name='highest_value',
            field=models.IntegerField(default=10, verbose_name='\u0623\u0639\u0644\u0649 \u062f\u0631\u062c\u0629 \u064a\u0645\u0643\u0646 \u0646\u064a\u0644\u0647\u0627'),
        ),
    ]
