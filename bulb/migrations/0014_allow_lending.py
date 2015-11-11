# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0013_readerprofile_submission_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='available_until',
            field=models.DateField(help_text='\u0627\u0644\u0643\u062a\u0627\u0628 \u0645\u062a\u0627\u062d \u0644\u0644\u0627\u0633\u062a\u0639\u0627\u0631\u0629 \u062d\u062a\u0649 \u062a\u0627\u0631\u064a\u062e \u0645\u062d\u062f\u062f (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', null=True, verbose_name='\u0645\u062a\u0627\u062d \u062d\u062a\u0649', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='contribution',
            field=models.CharField(default=b'G', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0645\u0633\u0627\u0647\u0645\u0629', choices=[(b'L', '\u0625\u0639\u0627\u0631\u0629'), (b'G', '\u0627\u0642\u062a\u0646\u0627\u0621')]),
        ),
        migrations.AddField(
            model_name='point',
            name='category',
            field=models.CharField(default=b'G', max_length=1, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641', choices=[(b'L', '\u0627\u0633\u062a\u0639\u0627\u0631\u0629'), (b'G', '\u0627\u0642\u062a\u0646\u0627\u0621')]),
        ),
        migrations.AddField(
            model_name='request',
            name='borrowing_end_date',
            field=models.DateField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0646\u062a\u0647\u0627\u0621 \u0645\u062f\u0629 \u0627\u0644\u0625\u0639\u0627\u0631\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='owner_status',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u062d\u0627\u0644\u0629 \u0635\u0627\u062d\u0628 \u0627\u0644\u0643\u062a\u0627\u0628', blank=True, choices=[(b'', '\u0645\u0639\u0644\u0642\u0629'), (b'D', '\u0633\u0644\u0645 \u0644\u0637\u0627\u0644\u0628\u0647'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649'), (b'R', '\u0623\u0639\u064a\u062f \u0628\u0639\u062f \u0627\u0644\u0625\u0639\u0627\u0631\u0629')]),
        ),
        migrations.AlterField(
            model_name='request',
            name='requester_status',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u062d\u0627\u0644\u0629 \u0645\u0642\u062f\u0645 \u0627\u0644\u0637\u0644\u0628', blank=True, choices=[(b'', '\u0645\u0639\u0644\u0642\u0629'), (b'D', '\u0633\u0644\u0645 \u0644\u0637\u0627\u0644\u0628\u0647'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649'), (b'R', '\u0623\u0639\u064a\u062f \u0628\u0639\u062f \u0627\u0644\u0625\u0639\u0627\u0631\u0629')]),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(default=b'', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629 \u0627\u0644\u0639\u0627\u0645\u0629', blank=True, choices=[(b'', '\u0645\u0639\u0644\u0642\u0629'), (b'D', '\u0633\u0644\u0645 \u0644\u0637\u0627\u0644\u0628\u0647'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649'), (b'R', '\u0623\u0639\u064a\u062f \u0628\u0639\u062f \u0627\u0644\u0625\u0639\u0627\u0631\u0629')]),
        ),
    ]
