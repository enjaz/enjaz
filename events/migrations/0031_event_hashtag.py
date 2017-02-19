# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_add_culture_program'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='hashtag',
            field=models.CharField(default=b'', help_text=b'\xd8\xa8\xd8\xaf\xd9\x88\xd9\x86 #', max_length=20, verbose_name='\u0647\u0627\u0634\u062a\u0627\u063a', blank=True),
        ),
    ]
