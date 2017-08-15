# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_studentclubyear_bookexchange_open_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=30, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629')),
            ],
            options={
                'verbose_name': '\u0645\u062f\u064a\u0646\u0629 \u062c\u0627\u0645\u0639\u064a\u0629',
                'verbose_name_plural': '\u0645\u062f\u0646 \u062c\u0627\u0645\u0639\u064a\u0629',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', choices=[(b'M', '\u0637\u0644\u0627\u0628'), (b'F', '\u0637\u0627\u0644\u0628\u0627\u062a')])),
                ('campus', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629 \u0627\u0644\u062c\u0627\u0645\u0639\u064a\u0629', to='core.Campus')),
            ],
            options={
                'verbose_name': '\u0642\u0650\u0633\u0645',
                'verbose_name_plural': '\u0623\u0642\u0633\u0627\u0645',
            },
        ),
    ]
