# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hpc', '0003_add_hpc_clubs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('clear_objectives', models.PositiveSmallIntegerField(verbose_name=b'Is the research Objective(s) clear?', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('informative_abstract', models.PositiveSmallIntegerField(verbose_name=b'Is title of the ABSTRACT informative!', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('introduction', models.PositiveSmallIntegerField(verbose_name=b'Does the introduction cover the topic of interest!', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('clear_method', models.PositiveSmallIntegerField(verbose_name=b'Is the method informative and clear!', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('good_statistics', models.PositiveSmallIntegerField(verbose_name=b'Are the statistical methods used well described and appropriate for the purpose of the study?', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('clear_sampling', models.PositiveSmallIntegerField(verbose_name=b'Is the sampling technique clear and suitable to the study?', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('clear_results', models.PositiveSmallIntegerField(verbose_name=b'Does the result section match the methods done? Is there a result for all methods described?', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('clear_discussion', models.PositiveSmallIntegerField(verbose_name=b'Is the discussion clear and answers the research question?', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('good_english', models.PositiveSmallIntegerField(verbose_name=b'What is your evaluation of the English language of this paper!', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('overall_evaluation', models.PositiveSmallIntegerField(verbose_name=b'What is your overall evaluation of this paper?', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
            ],
        ),
        migrations.AddField(
            model_name='abstract',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='abstract',
            field=models.OneToOneField(to='hpc.Abstract'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='evaluator',
            field=models.ForeignKey(related_name='abstract_evaluations', to=settings.AUTH_USER_MODEL),
        ),
    ]
