# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # We manusally added these dependencies because all of them
        # store city code instead of the full city name.  So they have
        # to be applied before this one.
        ('hpc', '0003_add_hpc_clubs'),
        ('researchhub', '0002_add_club'),
        ('events', '0013_add_2nd_hpc'),
        ('bulb', '0027_readathon_team'),
        ('studentguide', '0012_add_studentguide_clubs'),
        ('clubs', '0049_logo_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='city',
            field=models.CharField(max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[('\u0627\u0644\u0631\u064a\u0627\u0636', '\u0627\u0644\u0631\u064a\u0627\u0636'), ('\u062c\u062f\u0629', '\u062c\u062f\u0629'), ('\u0627\u0644\u0623\u062d\u0633\u0627\u0621', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
        migrations.AlterField(
            model_name='college',
            name='city',
            field=models.CharField(max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[('\u0627\u0644\u0631\u064a\u0627\u0636', '\u0627\u0644\u0631\u064a\u0627\u0636'), ('\u062c\u062f\u0629', '\u062c\u062f\u0629'), ('\u0627\u0644\u0623\u062d\u0633\u0627\u0621', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
        migrations.AlterField(
            model_name='team',
            name='city',
            field=models.CharField(default=b'', max_length=20, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True, choices=[('\u0627\u0644\u0631\u064a\u0627\u0636', '\u0627\u0644\u0631\u064a\u0627\u0636'), ('\u062c\u062f\u0629', '\u062c\u062f\u0629'), ('\u0627\u0644\u0623\u062d\u0633\u0627\u0621', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')]),
        ),
    ]
