# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_criteria(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    Criterion = apps.get_model('events', 'Criterion')
    hpc_r = Event.objects.get(code_name="hpc2-r")
    hpc_j = Event.objects.get(code_name="hpc2-j")
    hpc_a = Event.objects.get(code_name="hpc2-a")
    Criterion.objects.filter(code_name__in=['hpc2-1', 'hpc2-2',
                                            'hpc2-3', 'hpc2-4',
                                            'hpc2-5', 'hpc2-6',
                                            'hpc2-7', 'hpc2-8',
                                            'hpc2-9', 'hpc2-10']).delete()

    c1 = Criterion.objects.create(human_name='Is the title of the abstract informative?',
                                  code_name='hpc2-1')
    c2 = Criterion.objects.create(human_name='Is the research aim clear?',
                                  code_name='hpc2-2')
    c3 = Criterion.objects.create(human_name='Does the introduction cover the topic of interest?',
                                  code_name='hpc2-3')
    c4 = Criterion.objects.create(human_name='Is the method appropriate and clear?',
                                  code_name='hpc2-4')
    c5 = Criterion.objects.create(human_name='Are the results clear?',
                                  code_name='hpc2-5')
    c6 = Criterion.objects.create(human_name='Does the conclusions highlight the main results and challenges?',
                                  code_name='hpc2-6')
    c7 = Criterion.objects.create(human_name='Was the level of English satisfactory?',
                                  code_name='hpc2-7')

    for criterion in [c1, c2, c3, c4, c5, c6, c7]:
        criterion.events.add(hpc_r, hpc_a, hpc_j)

def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('events', 'Criterion')
    Criterion.objects.filter(code_name__in=['hpc2-1', 'hpc2-2',
                                            'hpc2-3', 'hpc2-4',
                                            'hpc2-5', 'hpc2-6',
                                            'hpc2-7']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('events', '0038_criterion_many_events'),
    ]

    operations = [
        migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
