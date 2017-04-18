# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def migrate_profiles(apps, schema_editor):
    OldTag = apps.get_model('arshidni', 'Tag')
    OldProfile = apps.get_model('arshidni', 'ColleagueProfile')
    NewTag = apps.get_model('studentguide', 'Tag')
    NewProfile = apps.get_model('studentguide', 'GuideProfile')
    NewRequest = apps.get_model('studentguide', 'Request')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    for old_profile in OldProfile.objects.filter(year=year_2015_2016):
        new_profile = NewProfile.objects.create(user=old_profile.user,
                                                academic_interests=old_profile.bio,
                                                nonacademic_interests=old_profile.interests,
                                                batch=old_profile.batch, year=year_2015_2016)
        new_profile.submission_date = old_profile.submission_date

        if old_profile.tags.filter(pk=1).exists():
            new_tag = NewTag.objects.get(code_name="first_year")
            new_profile.tags.add(new_tag)
        if old_profile.tags.filter(pk=2).exists():
            new_tag = NewTag.objects.get(code_name="second_year")
            new_profile.tags.add(new_tag)
        if old_profile.tags.filter(pk=4).exists():
            new_tag = NewTag.objects.get(code_name="research")
            new_profile.tags.add(new_tag)
        if old_profile.tags.filter(pk=5).exists():
            new_tag = NewTag.objects.get(code_name="international_exams")
            new_profile.tags.add(new_tag)
        if old_profile.tags.filter(pk=6).exists():
            new_tag = NewTag.objects.get(code_name="elective_training")
            new_profile.tags.add(new_tag)
        if old_profile.tags.filter(pk=7).exists():
            new_tag = NewTag.objects.get(code_name="extracurricular")
            new_profile.tags.add(new_tag)

        new_profile.save()

        for old_request in old_profile.supervision_requests.all():
            if old_request.status == 'P':
                guide_status = 'P'
                requester_status = 'A'
            elif old_request.status == 'A':
                guide_status = 'A'
                requester_status = 'A'
            elif old_request.status == 'R':
                guide_status = 'R'
                requester_status = 'A'
            elif old_request.status == 'D':
                guide_status = 'P'
                requester_status = 'C'
            elif old_request.status == 'WN':
                guide_status = 'A'
                requester_status = 'C'
            elif old_request.status == 'WC':
                guide_status = 'R'
                requester_status = 'A'
                
            new_request = NewRequest.objects.create(
                user=old_request.user, guide=new_profile,
                interests=old_request.interests,
                batch=old_request.batch, guide_status=guide_status,
                requester_status=requester_status)
            new_request.submission_date = old_request.submission_date
            new_request.save()

def remove_new_profiles(apps, schema_editor):
    NewProfile = apps.get_model('studentguide', 'GuideProfile')
    NewProfile.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0002_add_tags'),
    ]

    operations = [
       # This was commented out since this is the only thing that
       # requires the deprecated arshidni app.

       # migrations.RunPython(migrate_profiles,
       #                      reverse_code=remove_new_profiles)
    ]
