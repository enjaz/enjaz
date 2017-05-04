# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0055_abstract_did_presenter_attend'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numerical_value', models.IntegerField(null=True, verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0631\u0642\u0645\u064a\u0629', blank=True)),
                ('text_value', models.TextField(verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629 \u0627\u0644\u0646\u0635\u064a\u0629')),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0633\u0624\u0627\u0644', choices=[(b'O', '\u0633\u0624\u0627\u0644 \u0645\u0641\u062a\u0648\u062d'), (b'S', '\u0645\u0642\u064a\u0627\u0633')])),
                ('text', models.CharField(max_length=100, verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('survey', models.ForeignKey(related_name='survey_questions', verbose_name='\u0627\u0644\u0627\u0633\u062a\u0628\u064a\u0627\u0646', to='events.Survey')),
            ],
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='question',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0633\u0624\u0627\u0644', to='events.SurveyQuestion'),
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='session',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062c\u0644\u0633\u0629', blank=True, to='events.Session', null=True),
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='survey',
            field=models.ForeignKey(related_name='survey_sessions', verbose_name='\u0627\u0644\u0627\u0633\u062a\u0628\u064a\u0627\u0646', blank=True, to='events.Survey', null=True),
        ),
    ]
