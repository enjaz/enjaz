# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_add_presentaion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstract',
            name='authors',
            field=models.TextField(verbose_name='Name of authors', blank=True),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='presentaion_date',
            field=models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0639\u0631\u0636', blank=True),
        ),
    ]
