# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0035_invitation_linked_to_twitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='location',
            field=models.CharField(default=b'', max_length=200, verbose_name='\u0627\u0644\u0645\u0643\u0627\u0646', blank=True),
        ),
    ]
