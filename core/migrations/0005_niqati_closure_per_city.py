# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_studentclubyear_niqati_closure_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentclubyear',
            name='niqati_closure_date',
        ),
        migrations.AddField(
            model_name='studentclubyear',
            name='alahsa_closing_ceremony_date',
            field=models.DateField(null=True, verbose_name='\u0627\u0644\u062d\u0641\u0644 \u0627\u0644\u062e\u062a\u0627\u0645\u064a \u0641\u064a \u0627\u0644\u0623\u062d\u0633\u0627\u0621', blank=True),
        ),
        migrations.AddField(
            model_name='studentclubyear',
            name='alahsa_niqati_closure_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u063a\u0644\u0627\u0642 \u0646\u0642\u0627\u0637\u064a \u0641\u064a \u0627\u0644\u0623\u062d\u0633\u0627\u0621', blank=True),
        ),
        migrations.AddField(
            model_name='studentclubyear',
            name='jeddah_closing_ceremony_date',
            field=models.DateField(null=True, verbose_name='\u0627\u0644\u062d\u0641\u0644 \u0627\u0644\u062e\u062a\u0627\u0645\u064a \u0641\u064a \u062c\u062f\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='studentclubyear',
            name='jeddah_niqati_closure_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u063a\u0644\u0627\u0642 \u0646\u0642\u0627\u0637\u064a \u0641\u064a \u062c\u062f\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='studentclubyear',
            name='riyadh_closing_ceremony_date',
            field=models.DateField(null=True, verbose_name='\u0627\u0644\u062d\u0641\u0644 \u0627\u0644\u062e\u062a\u0627\u0645\u064a \u0641\u064a \u0627\u0644\u0631\u064a\u0627\u0636', blank=True),
        ),
        migrations.AddField(
            model_name='studentclubyear',
            name='riyadh_niqati_closure_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0625\u063a\u0644\u0627\u0642 \u0646\u0642\u0627\u0637\u064a \u0641\u064a \u0627\u0644\u0631\u064a\u0627\u0636', blank=True),
        ),
    ]
