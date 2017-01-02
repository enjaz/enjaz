# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_add_hpc2nd_in_RJA'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstract',
            name='was_presented_at_others',
            field=models.BooleanField(default=False, verbose_name='Have you presented this research in any other conference before?'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='was_presented_previously',
            field=models.BooleanField(default=False, verbose_name='Have you presented this research in a previous year of this conference?'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='was_published',
            field=models.BooleanField(default=False, verbose_name='Have you published this research?'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='discussion',
            field=models.TextField(default=b'', verbose_name='Discussion', blank=True),
        ),
    ]
