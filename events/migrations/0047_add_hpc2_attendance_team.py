# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_attendance_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)

    hpc_2_r_attendance_team = Team.objects.create(name="فريق تحضير مؤتمر التخصصات الصحية الثاني - الرياض",
                                                  code_name="hpc2-r-a", year=year_2016_2017,
                                                  city="R", gender="")
    hpc_2_j_attendance_team = Team.objects.create(name="فريق تحضير مؤتمر التخصصات الصحية الثاني - جدة",
                                       code_name="hpc2-j-a", year=year_2016_2017,
                                       city="J", gender="")
    hpc_2_a_attendance_team = Team.objects.create(name="فريق تحضير مؤتمر التخصصات الصحية الثاني - الأحساء",
                                       code_name="hpc2-a-a", year=year_2016_2017,
                                       city="A", gender="")
    Event.objects.filter(code_name="hpc2-r").update(attendance_team=hpc_2_r_attendance_team)
    Event.objects.filter(code_name="hpc2-j").update(attendance_team=hpc_2_j_attendance_team)
    Event.objects.filter(code_name="hpc2-a").update(attendance_team=hpc_2_a_attendance_team)


def remove_attendance_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Team.objects.filter(code_name__in=["hpc2-r-a", "hpc2-j-a","hpc2-a-a"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0046_event_attendance_fields'),
    ]

    operations = [
        migrations.RunPython(
            add_attendance_team,
            reverse_code=remove_attendance_team),
    ]
