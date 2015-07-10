# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def separate_deanship_presidency(apps, schema_editor):
    """No longer will we have lasting clubs.  All clubs, including the
presidency and the deanship should last only one year.  This will help
us separate presidency activities easier too."""

    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2014_2015 = StudentClubYear.objects.get(start_date__year=2014, end_date__year=2015)
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)

    # Archive the deanship, and create a deanship for the current year.
    deanship2014_2015 = Club.objects.get(english_name="Deanship of Student Affairs")
    deanship2014_2015.year = year2014_2015
    deanship2014_2015.save()
    deanship2015_2016 = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year2015_2016,
        email="studentsclub@ksau-hs.edu.sa",
        visible=False,
        can_review=True,
        city="R",
        )

    # Archive the presidency, and create a presidency for the current year.
    presidency2014_2015 = Club.objects.get(english_name="Presidency")
    presidency2014_2015.year = year2014_2015
    presidency2014_2015.save()
    presidency2015_2016 = Club.objects.create(
        name="رئاسة نادي الطلاب",
        english_name="Presidency",
        description="",
        year=year2015_2016,
        parent=deanship2015_2016,
        email="studentsclub@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        city="R",
        )

    # For National Guard Male, National Guard Female, Jeddah and
    # Al-Ahsa presidencies, add the year and update the parent.
    for club in Club.objects.filter(year=None, parent=presidency2014_2015):
        club.parent = presidency2015_2016
        club.year = year2015_2016
        club.save()

def unify_deanship_presidency(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2014_2015 = StudentClubYear.objects.get(start_date__year=2014, end_date__year=2015)
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)

    # One lasting deanshhip
    deanship2014_2015 = Club.objects.get(english_name="Deanship of Student Affairs", year=year2014_2015)
    deanship2014_2015.year = None
    deanship2014_2015.save()
    Club.objects.get(english_name="Deanship of Student Affairs", year=year2015_2016).delete()

    # One lasting presidency
    presidency2014_2015 = Club.objects.get(english_name="Presidency", year=year2014_2015)
    presidency2014_2015.year = None
    presidency2014_2015.save()
    presidency2015_2016 = Club.objects.get(english_name="Presidency", year=year2015_2016)

    # The National Guard Male, National Guard Female, Jeddah and
    # Al-Ahsa presidencies are lasting clubs and the children of a
    # lasting presidency.
    for club in Club.objects.filter(year=year2015_2016, parent=presidency2015_2016):
        club.parent = presidency2014_2015
        club.year = None
        club.save()

    presidency2015_2016.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0015_optional_description'),
    ]

    operations = [
       migrations.RunPython(
            separate_deanship_presidency,
            reverse_code=unify_deanship_presidency),
    ]
