# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0059_fix_typo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
        migrations.RemoveField(
            model_name='session',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='surveyanswer',
            name='date_submitted',
        ),
        migrations.RemoveField(
            model_name='surveyanswer',
            name='session',
        ),
        migrations.RemoveField(
            model_name='surveyanswer',
            name='user',
        ),
        migrations.AlterField(
            model_name='session',
            name='mandatory_survey',
            field=models.ForeignKey(related_name='mandatory_sessions', verbose_name='\u0627\u0633\u062a\u0628\u064a\u0627\u0646 \u0625\u062c\u0628\u0627\u0631\u064a', blank=True, to='events.Survey', null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='optional_survey',
            field=models.ForeignKey(related_name='optional_sessions', verbose_name='\u0627\u0633\u062a\u0628\u064a\u0627\u0646 \u0627\u062e\u062a\u064a\u0627\u0631\u064a', blank=True, to='events.Survey', null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645'),
        ),
        migrations.AddField(
            model_name='surveyresponse',
            name='session',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062c\u0644\u0633\u0629', blank=True, to='events.Session', null=True),
        ),
        migrations.AddField(
            model_name='surveyresponse',
            name='survey',
            field=models.ForeignKey(related_name='responses', verbose_name='\u0627\u0644\u0627\u0633\u062a\u0628\u064a\u0627\u0646', blank=True, to='events.Survey', null=True),
        ),
        migrations.AddField(
            model_name='surveyresponse',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='survey_response',
            field=models.ForeignKey(related_name='answers', verbose_name='\u0627\u0633\u062a\u0628\u064a\u0627\u0646 \u0645\u0639\u0628\u0623', to='events.SurveyResponse', null=True),
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='is_english',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u0633\u0624\u0627\u0644 \u0625\u0646\u062c\u0644\u064a\u0632\u064a'),
        ),
    ]
