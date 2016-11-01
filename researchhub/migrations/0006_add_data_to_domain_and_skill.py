# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_domains(apps, schema_editor):
    Domain = apps.get_model('researchhub', 'Domain')

    if not Domain.objects.exists():
        Domain.objects.create(name="Basic Sciences")
        Domain.objects.create(name="Clinical Sciences")

def remove_domains(apps, schema_editor):
    Domain = apps.get_model('researchhub', 'Domain')
    Domain.objects.filter(name=["Basic Sciences", "Clinical Sciences"
                                ]).delete()

def add_skills(apps, schema_editor):
    Skill = apps.get_model('researchhub', 'Skill')

    if not Skill.objects.exists():
        Skill.objects.create(name="Data Entry")
        Skill.objects.create(name="Data Collection")
        Skill.objects.create(name="Manuscript Writing")
        Skill.objects.create(name="Proposal Writing")
        Skill.objects.create(name="Literature Review")
        Skill.objects.create(name="Data Analysis")
        Skill.objects.create(name="Lab Experience")

def remove_skills(apps, schema_editor):
    Skill = apps.get_model('researchhub', 'Skill')
    Skill.objects.filter(name=["Data Entry", "Data Collection",
                                        "Manuscript Writing", "Proposal Writing",
                                        "Literature Review", "Data Analysis",
                                        "Lab Experience"
                                        ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0005_add_domain_and_skill'),
    ]

    operations = [
       migrations.RunPython(
            add_domains,
            reverse_code=remove_domains),
       migrations.RunPython(
            add_skills,
            reverse_code=remove_skills),
    ]
