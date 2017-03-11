# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_criteria(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Criterion = apps.get_model('events', 'Criterion')
    event= Event.objects.get(code_name="hpc2-r")
    Criterion.objects.create(event=event,human_name='Is the research objective(s) clear ?',code_name='hpc2-1',instructions='')
    Criterion.objects.create(event=event,human_name='Is the title of the abstract informative ?',code_name='hpc2-2',instructions='')
    Criterion.objects.create(event=event,human_name='Does the introduction cover the topic of interest?',code_name='hpc2-3',instructions='')
    Criterion.objects.create(event=event,human_name='Is the method informative and clear ?',code_name='hpc2-4',instructions='')
    Criterion.objects.create(event=event,human_name='Are the statistical methods used well described and appropriate for the purpose of the study ? ',code_name='hpc2-5',instructions='')
    Criterion.objects.create(event=event,human_name='Is the sampling technique clear and suitable for the study ?',code_name='hpc2-6',instructions='')
    Criterion.objects.create(event=event,human_name='Does the results section match the methods done ? Is there a result for all the methods described ?',code_name='hpc2-7',instructions='')
    Criterion.objects.create(event=event,human_name='Is the discussion clear and answers the research question ?',code_name='hpc2-8',instructions='')
    Criterion.objects.create(event=event,human_name='What is the evaluation of the English language of this paper ?',code_name='hpc2-9',instructions='')
    Criterion.objects.create(event=event,human_name='What is the overall evaluation of this paper ?',code_name='hpc2-10',instructions='')

def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('events', 'Criterion')
    Criterion.objects.filter(code_name__in=['hpc2-1','hpc2-2','hpc2-3','hpc2-4','hpc2-5','hpc2-6','hpc2-7','hpc2-8','hpc2-9','hpc2-10']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_add_evaluation_team'),
    ]
    
    operations = [
        migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
