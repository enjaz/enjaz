# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_studentclubyear_bookexchange_open_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselSlider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629')),
                ('alt', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0646\u0635 \u0627\u0644\u0628\u062f\u064a\u0644', blank=True)),
            ],
        ),
    ]
