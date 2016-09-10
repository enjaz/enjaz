# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_deanships(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    jeddah_presidency = Club.objects.get(english_name="Presidency", city="J",
                                         year=year_2016_2017)
    alahsa_presidency = Club.objects.get(english_name="Presidency", city="A",
                                         year=year_2016_2017)

    # Naming patern:
    # <city>_<college>_<gender>_<deanship or club>


    # Al-Ahsa clubs
    a_a_m_c = Club.objects.get(english_name="College of Applied Medical Sciences",
                               gender="M", city="A",
                               year=year_2016_2017)
    a_a_f_c = Club.objects.get(english_name="College of Applied Medical Sciences",
                               gender="F", city="A",
                               year=year_2016_2017)
    a_n_f_c = Club.objects.get(english_name="College of Nursing",
                               gender="F", city="A",
                               year=year_2016_2017)

    # Jeddah clubs
    j_m_m_c = Club.objects.get(english_name="College of Medicine",
                               gender="M", year=year_2016_2017,
                               city="J")
    j_m_f_c = Club.objects.get(english_name="College of Medicine",
                               gender="F", year=year_2016_2017,
                               city="J")
    j_n_f_c = Club.objects.get(english_name="College of Nursing",
                               gender="F", year=year_2016_2017,
                               city="J")
    j_b_m_c = Club.objects.get(english_name="College of Science and Health Professions",
                               gender="M",
                               year=year_2016_2017,
                               city="J")
    j_b_f_c = Club.objects.get(english_name="College of Science and Health Professions",
                               gender="F",
                               year=year_2016_2017, city="J")

    
    # Al-Ahsa deanships
    a_a_m_d = Club.objects.create(name="عمادة كلية العلوم الطبية التطبيقية",
                                  english_name="Deanship of the College of Applied Medical Sciences",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=alahsa_presidency,
                                  gender="M",
                                  city="A",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    a_a_m_c.parent = a_a_m_d
    a_a_m_c.save()
    a_a_f_d = Club.objects.create(name="عمادة كلية العلوم الطبية التطبيقية",
                                  english_name="Deanship of the College of Applied Medical Sciences",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=alahsa_presidency,
                                  gender="F",
                                  city="A",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    a_a_f_c.parent = a_a_f_d
    a_a_f_c.save()
    a_n_f_d = Club.objects.create(name="عمادة كلية التمريض",
                                  english_name="Deanship of the College of Nursing",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=alahsa_presidency,
                                  gender="F",
                                  city="A",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    a_n_f_c.parent = a_n_f_d
    a_n_f_c.save()

    # Jeddah deanships
    j_m_m_d = Club.objects.create(name="عمادة كلية الطب",
                                  english_name="Deanship of the College of Medicine",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=jeddah_presidency,
                                  gender="M",
                                  city="J",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    j_m_m_c.parent = j_m_m_d
    j_m_m_c.save()
    j_m_f_d = Club.objects.create(name="عمادة كلية الطب",
                                  english_name="Deanship of the College of Medicine",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=jeddah_presidency,
                                  gender="F",
                                  city="J",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    j_m_f_c.parent = j_m_f_d
    j_m_f_c.save()
    j_n_f_d = Club.objects.create(name="عمادة كلية التمريض",
                                  english_name="Deanship of the College of Nursing",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=jeddah_presidency,
                                  gender="F",
                                  city="J",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    j_n_f_c.parent = j_n_f_d
    j_n_f_c.save()
    j_b_m_d = Club.objects.create(name="عمادة كلية العلوم والمهن الصحية",
                                  english_name="Deanship of the College of Science and Health Professions",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=jeddah_presidency,
                                  gender="M",
                                  city="J",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    j_b_m_c.parent = j_b_m_d
    j_b_m_c.save()
    j_b_f_d = Club.objects.create(name="عمادة كلية العلوم والمهن الصحية",
                                  english_name="Deanship of the College of Science and Health Professions",
                                  description="",
                                  email="pending@ksau-hs.edu.sa",
                                  parent=jeddah_presidency,
                                  gender="F",
                                  city="J",
                                  year=year_2016_2017,
                                  visible=False,
                                  can_review=True,
                                  can_delete=False,
                                  can_edit=False)
    j_b_f_c.parent = j_b_f_d
    j_b_f_c.save()

    # Let's talk about specialized club in Al-Ahsa; those that don't
    # have a college.
    alhsa_deanships = [a_a_m_d, a_a_f_d, a_n_f_d]
    for alahsa_child in alahsa_presidency.children.filter(college__isnull=True):
        if alahsa_child in alhsa_deanships:
            continue
        alahsa_child.possible_parents.add(*alhsa_deanships)
        alahsa_child.save()

    # Let's talk about specialized club in Jeddah.
    jeddah_deanships = [j_m_m_d, j_m_f_d, j_n_f_d, j_b_m_d, j_b_f_d]
    for jeddah_child in jeddah_presidency.children.filter(college__isnull=True):
        if jeddah_child in jeddah_deanships:
            continue
        jeddah_child.possible_parents.add(*jeddah_deanships)
        jeddah_child.save()

def remove_deanships(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0043_add_2016_clubs'),
    ]

    operations = [
       migrations.RunPython(add_deanships)
    ]
