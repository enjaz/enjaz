# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    
    # Reforming presidency
    alahsa_deanship = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year_2016_2017,
        email="studentsclub@ksau-hs.edu.sa",
        visible=False,
        can_review=True,
        can_view_assessments=False,
        is_assessed=False,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city="A",
        )
    riyadh_deanship = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year_2016_2017,
        email="studentsclub@ksau-hs.edu.sa",
        visible=False,
        can_review=True,
        can_view_assessments=False,
        is_assessed=False,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city="R",
        )
    presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                     year=year_2016_2017,
                                     english_name="Presidency",
                                     description="",
                                     email="studentsclub@ksau-hs.edu.sa",
                                     parent=riyadh_deanship,
                                     can_review=False,
                                     visible=False,
                                     is_assessed=False,
                                     city="R")
    male_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                          year=year_2016_2017,
                                          english_name="Presidency",
                                          description="",
                                          email="sc-m@ksau-hs.edu.sa",
                                          parent=presidency,
                                          can_review=True,
                                          visible=False,
                                          is_assessed=False,
                                          gender="M",
                                          city="R")
    female_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                            year=year_2016_2017,
                                            english_name="Presidency",
                                            description="",
                                            email="sc-m@ksau-hs.edu.sa",
                                            parent=presidency,
                                            can_review=True,
                                            visible=False,
                                            is_assessed=False,
                                            gender="F",
                                            city="R")
    jeddah_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                            year=year_2016_2017,
                                            english_name="Presidency",
                                            description="",
                                            email="sc-j@ksau-hs.edu.sa",
                                            parent=presidency,
                                            can_review=True,
                                            visible=False,
                                            is_assessed=False,
                                            city="J")
    alahsa_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                            year=year_2016_2017,
                                            english_name="Presidency",
                                            description="",
                                            email="sc-ah@ksau-hs.edu.sa",
                                            parent=alahsa_deanship,
                                            can_review=True,
                                            visible=False,
                                            is_assessed=False,
                                            city="A")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency, 
        description="",
        year=year_2016_2017,
        email="sc-media@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        gender="F",
        city="R")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency, 
        description="",
        year=year_2016_2017,
        email="sc-media@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        gender="M",
        city="R")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency, 
        description="",
        year=year_2016_2017,
        email="sc-mediaj@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city="J")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency, 
        description="",
        year=year_2016_2017,
        email="sc-mediaah@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city="A")

    # Variables are named: <city_code>_<college_code>_<gender_code>.

    # Rriyadh Colleges
    r_m_m = College.objects.get(name='M', section='NG', city='R',
                                gender='M')
    r_d_m = College.objects.get(name='D', section='NG', city='R',
                                gender='M')
    r_p_m = College.objects.get(name='P', section='NG', city='R',
                                gender='M')
    r_a_m = College.objects.get(name='A', section='NG', city='R',
                                gender='M')
    r_i_m = College.objects.get(name='I', section='NG', city='R',
                                gender='M')
    r_b_m = College.objects.get(name='B', section='NG', city='R',
                                gender='M')
    r_m_f = College.objects.get(name='M', section='NG', city='R',
                                gender='F')
    r_d_f = College.objects.get(name='D', section='NG', city='R',
                                gender='F')
    r_p_f = College.objects.get(name='P', section='NG', city='R',
                                gender='F')
    r_a_f = College.objects.get(name='A', section='NG', city='R',
                                gender='F')
    r_b_f = College.objects.get(name='B', section='NG', city='R',
                                gender='F')
    r_n_f = College.objects.get(name='N', section='NG', city='R',
                                gender='F')
    # Al-Ahsa colleges
    a_a_m = College.objects.get(name='A', section='A', city='A',
                                gender='M')
    a_a_f = College.objects.get(name='A', section='A', city='A',
                                gender='F')
    a_n_f = College.objects.get(name='N', section='A', city='A',
                                gender='F')
    # Jeddah Colleges
    j_m_m = College.objects.get(name='M', section='J', city='J',
                                gender='M')
    j_m_f = College.objects.get(name='M', section='J', city='J',
                                gender='M')
    j_n_f = College.objects.get(name='N', section='J', city='J',
                                gender='F')
    j_b_m = College.objects.get(name='B', section='J', city='J',
                                gender='M')
    j_b_f = College.objects.get(name='B', section='J', city='J',
                                gender='F')

    # Riyadh clubs
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="",
                        email="sc-coshp@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R",
                        college=r_b_m)
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="",
                        email="sc-coshpf@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R",
                        college=r_b_f)
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="",
                        email="sc-com@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R",
                        college=r_m_m)
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="",
                        email="sc-com@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R",
                        college=r_m_f)
    Club.objects.create(name="كلية طب الأسنان",
                        english_name="College of Dentistry",
                        description="",
                        email="sc-cod@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R",
                        college=r_d_m)
    Club.objects.create(name="كلية طب الأسنان",
                        english_name="College of Dentistry",
                        description="",
                        email="sc-codf@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R",
                        college=r_d_f)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="",
                        email="sc-cams@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R",
                        college=r_a_m)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="",
                        email="sc-camsf@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R",
                        college=r_a_f)
    Club.objects.create(name="كلية الصيدلة",
                        english_name="College of Pharmacy",
                        description="",
                        email="sc-cop@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R",
                        college=r_p_m)
    Club.objects.create(name="كلية الصيدلة",
                        english_name="College of Pharmacy",
                        description="",
                        email="sc-cop@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R",
                        college=r_p_f)
    Club.objects.create(name="كلية الصحة العامة والمعلوماتية الصحية",
                        english_name="College of Public Health and Health Informatics",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R",
                        college=r_i_m)
    Club.objects.create(name="كلية التمريض",
                        english_name="College of Nursing",
                        description="",
                        email="sc-conr@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R",
                        college=r_n_f)
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="",
                        email="bestnation.club@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="",
                        email="bestnation.club@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي البحث والابتكار والتقنية",
                        english_name="Research, Innovation and Technology Club",
                        description="",
                        email="researchclub@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="LeenClub@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="LeenClub@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="",
                        email="arshidny@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="R")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidny",
                        description="",
                        email="arshidny@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="R")

    # Jeddah clubs
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="",
                        email="sc-comj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="J",
                        college=j_m_m)
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="",
                        email="sc-comj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="J",
                        college=j_m_f)
    Club.objects.create(name="كلية التمريض",
                        english_name="College of Nursing",
                        description="",
                        email="sc-conj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="J",
                        college=j_n_f)
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="",
                        email="sc-coshpj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="J",
                        college=j_b_m)
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="",
                        email="sc-coshpfj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="J",
                        college=j_b_f)
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="J")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="",
                        email="bestnation.club-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="J")
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="J")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="leenclub-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="J")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="",
                        email="arshidny-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="J")

    # Al-Ahsa clubs
    Club.objects.create(name="كلية التمريض",
                        english_name="College of Nursing",
                        description="",
                        email="sc-conah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="A",
                        college=a_n_f)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="",
                        email="sc-cams@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="M",
                        year=year_2016_2017,
                        city="A",
                        college=a_a_m)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="",
                        email="sc-camsf@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="F",
                        year=year_2016_2017,
                        city="A",
                        college=a_a_f)
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.clubah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="A")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="",
                        email="bestnation.clubah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="A")
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub-ah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="A")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="leenclub.ah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="A")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="",
                        email="arshidny-a@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="A")

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)

    Club.objects.filter(year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0042_alahsa_deanship'),
        ('core', '0006_add_2016_year'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
