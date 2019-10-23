# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_booth_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstract',
            name='introduction',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='methodology',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='was_presented_at_others',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='was_presented_previously',
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='was_published',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='clinical_presentation',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='diagnosis',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='introduction',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='outcome',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='patient_info',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='treatment',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='was_presented_at_others',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='was_presented_previously',
        ),
        migrations.RemoveField(
            model_name='casereport',
            name='was_published',
        ),
        migrations.AddField(
            model_name='abstract',
            name='background',
            field=models.TextField(default=b'', verbose_name='Background'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='conference_presented_at',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Name of the conference presented at'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='gender',
            field=models.CharField(max_length=1, null=True, verbose_name=b'Gender', choices=[(b'F', b'Female'), (b'M', b'Male')]),
        ),
        migrations.AddField(
            model_name='abstract',
            name='graduation_year',
            field=models.CharField(default=b'', max_length=4, verbose_name=b'when did you graduate/expected year of graduation'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='irb_approval',
            field=models.CharField(default=b'N', max_length=1, verbose_name=b'Do you have an IRB Approval?', choices=[(b'N', b'No'), (b'Y', b'Yes')]),
        ),
        migrations.AddField(
            model_name='abstract',
            name='methods',
            field=models.TextField(default=b'', verbose_name='Methods'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='principle_investigator',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Principle Investigator'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='significance',
            field=models.TextField(default=b'', verbose_name='How is your study going to affect current practice?'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='study_design',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Study Design'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='submitted_to_journal',
            field=models.CharField(default=b'N', max_length=1, null=True, verbose_name=b'Have you submitted the manuscript of this study to a journal before?', choices=[(b'N', b'No'), (b'P', b'Yes, Published'), (b'U', b'Yes, Under Revision')]),
        ),
        migrations.AddField(
            model_name='abstract',
            name='was_presented_at_conference',
            field=models.BooleanField(default=False, verbose_name='Has the study been presented in a conference before?'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='background',
            field=models.TextField(default=b'', verbose_name='Background'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='case_description',
            field=models.TextField(default=b'', verbose_name='Case Description'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='conference_presented_at',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Name of the conference presented at'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='gender',
            field=models.CharField(default=b'M', max_length=1, verbose_name=b'Gender', choices=[(b'F', b'Female'), (b'M', b'Male')]),
        ),
        migrations.AddField(
            model_name='casereport',
            name='graduation_year',
            field=models.CharField(default=b'', max_length=4, verbose_name=b'when did you graduate/ expected year of graduation'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='principle_investigator',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Principle Investigator'),
        ),
        migrations.AddField(
            model_name='casereport',
            name='was_presented_at_conference',
            field=models.BooleanField(default=False, verbose_name='Has the study been presented in a conference before?'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='college',
            field=models.CharField(max_length=255, verbose_name=b'Department/College'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='level',
            field=models.CharField(default=b'', max_length=1, verbose_name=b'Level', blank=True, choices=[(b'U', b'Undergraduate'), (b'G', b'Graduate')]),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='study_field',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Study Field'),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='university',
            field=models.CharField(max_length=255, verbose_name=b'Institution/University'),
        ),
        migrations.AlterField(
            model_name='casereport',
            name='college',
            field=models.CharField(max_length=255, verbose_name=b'Department/College'),
        ),
        migrations.AlterField(
            model_name='casereport',
            name='study_field',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Study Field'),
        ),
        migrations.AlterField(
            model_name='casereport',
            name='university',
            field=models.CharField(max_length=255, verbose_name=b'Institution/University'),
        ),
    ]
