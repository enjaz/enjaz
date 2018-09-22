# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_add_child_survy'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='collection_method',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Data Collection Method'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='category',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'M', b'College of Medicine'), (b'D', b'College of Dentistry'), (b'P', b'College of Pharmacy')]),
        ),
        migrations.AlterField(
            model_name='usersurveycategory',
            name='category',
            field=models.CharField(max_length=1, verbose_name=b'chose your studying profession', choices=[(b'M', b'College of Medicine'), (b'D', b'College of Dentistry'), (b'P', b'College of Pharmacy')]),
        ),
    ]
