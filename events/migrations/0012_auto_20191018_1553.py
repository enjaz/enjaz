# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20191018_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseReportAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name of authors', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='casereport',
            name='authors',
            field=models.TextField(verbose_name='Name of authors', blank=True),
        ),
        migrations.AlterField(
            model_name='casereport',
            name='level',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'Level', blank=True, choices=[(b'U', b'Undergraduate'), (b'G', b'Graduate')]),
        ),
        migrations.AlterField(
            model_name='casereport',
            name='was_presented_at_conference',
            field=models.CharField(default=b'N', max_length=1, verbose_name=b'Has the case report been presented in a conference before?', choices=[(b'N', b'No'), (b'Y', b'Yes')]),
        ),
        migrations.AddField(
            model_name='casereportauthor',
            name='case_report',
            field=models.ForeignKey(related_name='author', to='events.CaseReport'),
        ),
    ]
