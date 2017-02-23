# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def get_invisible_clubs(apps):
    Club = apps.get_model("clubs", "Club")
    media_center = Club.objects.get(english_name="Media Center")
    presidency = Club.objects.get(english_name="Presidency")
    dsa = Club.objects.get(english_name="Deanship of Student Affairs")
    return media_center, presidency, dsa

def upgrade_clubs(apps, schema_editor):
    Club = apps.get_model("clubs", "Club")
    media_center, presidency, dsa = get_invisible_clubs(apps)

    media_center.parent = presidency
    media_center.save()

    presidency.parent = dsa
    presidency.save()

    male_presidency = Club.objects.create(name=u"رئاسة نادي الطلاب (طلاب)",
                          english_name="Presidency (Male)",
                          description="",
                          email="sc-m@ksau-hs.edu.sa",
                          city="الرياض",
                          visible=False,
                          can_review=True,
                          parent=presidency,  # assign parent
                       )
    female_presidency = Club.objects.create(name=u"رئاسة نادي الطلاب (طالبات)",
                          english_name="Presidency (Female)",
                          description="",
                          email="sc-f@ksau-hs.edu.sa",
                          city="الرياض",
                          visible=False,
                          can_review=True,
                          parent=presidency,  # assign parent
                       )

def downgrade_clubs(apps, schema_editor):
    Club = apps.get_model("clubs", "Club")
    media_center, presidency, dsa = get_invisible_clubs(apps)

    media_center.parent = None
    media_center.save()

    presidency.parent = None
    presidency.save()

    female_presidency = Club.objets.get(english_name="Presidency (Female)")
    female_presidency.delete()
    male_presidency = Club.objets.get(english_name="Presidency (Male)")
    male_presidency.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_add_dsa'),
    ]

    operations = [
       migrations.RunPython(
            upgrade_clubs,
            reverse_code=downgrade_clubs),
    ]
