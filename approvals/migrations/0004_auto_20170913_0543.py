# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_auto_20170901_0524'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0015_merge'),
        ('approvals', '0003_auto_20170911_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequirementRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, verbose_name='\u0627\u0644\u0648\u0635\u0641')),
            ],
            options={
                'verbose_name': '\u0645\u062a\u0637\u0644\u0651\u0628',
                'verbose_name_plural': '\u0645\u062a\u0637\u0644\u0651\u0628\u0627\u062a',
            },
        ),
        migrations.AddField(
            model_name='activitycancelrequest',
            name='submitter',
            field=models.ForeignKey(related_name='activitycancelrequests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0645\u0642\u062f\u0651\u0645 \u0627\u0644\u0637\u0644\u0628', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='activitycancelrequest',
            name='submitter_team',
            field=models.ForeignKey(related_name='activitycancelrequests', default=1, verbose_name='\u0627\u0644\u0641\u0631\u064a\u0642 \u0627\u0644\u0645\u0642\u062f\u0651\u0645 \u0644\u0644\u0637\u0644\u0628', to='teams.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='campus',
            field=models.ManyToManyField(to='core.Campus'),
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='category',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='collaborating_teams',
            field=models.ManyToManyField(related_name='collaborated_activity_requests', verbose_name='\u0627\u0644\u0641\u0631\u0642 \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0629', to='teams.Team'),
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='description',
            field=models.TextField(default='', verbose_name='\u0627\u0644\u0648\u0635\u0641'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='gender',
            field=models.CharField(default='', max_length=1, choices=[(b'M', '\u0627\u0644\u0637\u0644\u0627\u0628'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='goals',
            field=models.TextField(default='', verbose_name='\u0627\u0644\u0623\u0647\u062f\u0627\u0641'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='inside_collaborators',
            field=models.TextField(default='', verbose_name='\u0627\u0644\u062c\u0647\u0627\u062a \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0629 \u0645\u0646 \u062f\u0627\u062e\u0644 \u0627\u0644\u062c\u0627\u0645\u0639\u0629'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='organizer_count',
            field=models.PositiveIntegerField(default=0, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='outside_collaborators',
            field=models.TextField(default='', verbose_name='\u0627\u0644\u062c\u0647\u0627\u062a \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0629 \u0645\u0646 \u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='participant_count',
            field=models.PositiveIntegerField(default=0, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='specialty',
            field=models.ManyToManyField(to='core.Specialty'),
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='submitter',
            field=models.ForeignKey(related_name='activityrequests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0645\u0642\u062f\u0651\u0645 \u0627\u0644\u0637\u0644\u0628', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='submitter_team',
            field=models.ForeignKey(related_name='activityrequests', default=1, verbose_name='\u0627\u0644\u0641\u0631\u064a\u0642 \u0627\u0644\u0645\u0642\u062f\u0651\u0645 \u0644\u0644\u0637\u0644\u0628', to='teams.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementrequest',
            name='activity_request',
            field=models.ForeignKey(related_name='requirementrequests', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637', to='approvals.ActivityRequest'),
        ),
    ]
