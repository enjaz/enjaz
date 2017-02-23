# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_teams(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    bulb_riyadh_male = Club.objects.get(english_name="Bulb",
                                        year=year_2016_2017, city="الرياض",
                                        gender='M')
    bulb_riyadh_female = Club.objects.get(english_name="Bulb",
                                          year=year_2016_2017, city="الرياض",
                                          gender='F')
    bulb_jeddah = Club.objects.get(english_name="Bulb",
                                   year=year_2016_2017, city="J",
                                   gender='')
    bulb_alahsa = Club.objects.get(english_name="Bulb",
                                   year=year_2016_2017, city="A",
                                   gender='')

    Team.objects.create(name="فريق المكتبة الطلابية التعاونية",
                        code_name="book_exchange",
                        year=year_2016_2017,
                        club=bulb_riyadh_male,
                        city="الرياض",
                        gender="M")
    Team.objects.create(name="فريق المكتبة الطلابية التعاونية",
                        code_name="book_exchange",
                        year=year_2016_2017,
                        club=bulb_riyadh_female,
                        city="الرياض",
                        gender="F")
    Team.objects.create(name="فريق المكتبة الطلابية التعاونية",
                        code_name="book_exchange",
                        year=year_2016_2017,
                        club=bulb_jeddah,
                        city="J",
                        gender="M")
    Team.objects.create(name="فريق المكتبة الطلابية التعاونية",
                        code_name="book_exchange",
                        year=year_2016_2017,
                        club=bulb_jeddah,
                        city="J",
                        gender="F")
    Team.objects.create(name="فريق المكتبة الطلابية التعاونية",
                        code_name="book_exchange",
                        year=year_2016_2017,
                        club=bulb_alahsa,
                        city="A",
                        gender="M")
    Team.objects.create(name="فريق المكتبة الطلابية التعاونية",
                        code_name="book_exchange",
                        year=year_2016_2017,
                        club=bulb_alahsa,
                        city="A",
                        gender="F")


def remove_teams(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Team.objects.filter(code_name="book_exchange",
                        year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0020_newspapersignup'),
        ('clubs', '0047_team'),
    ]

    operations = [
       migrations.RunPython(
            add_teams,
            reverse_code=remove_teams),
    ]
