# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_common_profiles(apps, schema_editor):
    CommonProfile = apps.get_model('accounts', 'CommonProfile')
    StudentProfile = apps.get_model('accounts', 'StudentProfile')
    NonStudentProfile = apps.get_model('accounts', 'NonStudentProfile')

    for student_profile in StudentProfile.objects.all():
        CommonProfile.objects.create(user=student_profile.user,
                                     is_student=True,
                                     ar_first_name=student_profile.ar_first_name,
                                     ar_middle_name=student_profile.ar_middle_name,
                                     ar_last_name=student_profile.ar_last_name,
                                     en_first_name=student_profile.en_first_name,
                                     en_middle_name=student_profile.en_middle_name,
                                     en_last_name=student_profile.en_last_name,
                                     badge_number=student_profile.badge_number,
                                     mobile_number=student_profile.mobile_number,
                                     city=student_profile.college.city,
                                     student_id=student_profile.student_id,
                                     college=student_profile.college,
                                     job_description="")
        student_profile.delete()
    #StudentProfile.objects.all().delete()

    for nonstudent_profile in NonStudentProfile.objects.all():
        CommonProfile.objects.create(user=nonstudent_profile.user,
                                     is_student=False,
                                     ar_first_name=nonstudent_profile.ar_first_name,
                                     ar_middle_name=nonstudent_profile.ar_middle_name,
                                     ar_last_name=nonstudent_profile.ar_last_name,
                                     en_first_name=nonstudent_profile.en_first_name,
                                     en_middle_name=nonstudent_profile.en_middle_name,
                                     en_last_name=nonstudent_profile.en_last_name,
                                     badge_number=nonstudent_profile.badge_number,
                                     mobile_number=nonstudent_profile.mobile_number,
                                     city="R",
                                     college=None,
                                     job_description=nonstudent_profile.job_description)
        nonstudent_profile.delete()
    #NonStudentProfile.objects.all().delete()

def delete_common_profiles(apps, schema_editor):
    CommonProfile = apps.get_model('accounts', 'CommonProfile')
    StudentProfile = apps.get_model('accounts', 'StudentProfile')
    NonStudentProfile = apps.get_model('accounts', 'NonStudentProfile')

    for common_profile in CommonProfile.objects.all():
        if common_profile.is_student:
            StudentProfile.objects.create(user=common_profile.user,
                                          ar_first_name=common_profile.ar_first_name,
                                          ar_middle_name=common_profile.ar_middle_name,
                                          ar_last_name=common_profile.ar_last_name,
                                          en_first_name=common_profile.en_first_name,
                                          en_middle_name=common_profile.en_middle_name,
                                          en_last_name=common_profile.en_last_name,
                                          badge_number=common_profile.badge_number,
                                          mobile_number=common_profile.mobile_number,
                                          student_id=common_profile.student_id,
                                          college=common_profile.college)
        else:
            NonStudentProfile.objects.create(user=common_profile.user,
                                             ar_first_name=common_profile.ar_first_name,
                                             ar_middle_name=common_profile.ar_middle_name,
                                             ar_last_name=common_profile.ar_last_name,
                                             en_first_name=common_profile.en_first_name,
                                             en_middle_name=common_profile.en_middle_name,
                                             en_last_name=common_profile.en_last_name,
                                             badge_number=common_profile.badge_number,
                                             mobile_number=common_profile.mobile_number,
                                             job_description=common_profile.job_description)
        common_profile.delete()
    #CommonProfile.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_commonprofile'),
    ]

    operations = [
       migrations.RunPython(
            create_common_profiles,
            reverse_code=delete_common_profiles),
    ]
