# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    presidency = Club.objects.get(english_name="Presidency")
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)

    # Reforming presidency
    male_presidency = Club.objects.get(english_name="Presidency (Male)")
    male_presidency.name = "رئاسة نادي الطلاب (الرياض/طلاب)"
    male_presidency.english_name = "Presidency (Riyadh/Male)"
    male_presidency.save()
    female_presidency = Club.objects.get(english_name="Presidency (Female)")
    female_presidency.name = "رئاسة نادي الطلاب (الرياض/طالبات)"
    female_presidency.english_name = "Presidency (Riyadh/Female)"
    female_presidency.save()
    jeddah_presidency = Club.objects.create(name="رئاسة نادي الطلاب (جدة)",
                                            english_name="Presidency (Jeddah)",
                                            description="-",
                                            email="sc-j@ksau-hs.edu.sa",
                                            parent=presidency,
                                            can_review=True,
                                            visible=False,
                                            city="J")
    alahsa_presidency = Club.objects.create(name="رئاسة نادي الطلاب (الأحساء)",
                                            english_name="Presidency (Al-Ahsa)",
                                            description="-",
                                            email="sc-ah@ksau-hs.edu.sa",
                                            parent=presidency,
                                            can_review=True,
                                            visible=False,
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
    j_n_f = College.objects.get(name='N', section='J', city='J',
                                gender='F')
    j_b_m = College.objects.get(name='B', section='J', city='J',
                                gender='M')
    j_b_f = College.objects.get(name='B', section='J', city='J',
                                gender='F')
    
    # Riyadh clubs
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="-",
                        email="sc-coshp@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R",
                        college=r_b_m)
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="-",
                        email="sc-coshpf@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_b_f)
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="-",
                        email="sc-com@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R",
                        college=r_m_m)
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="-",
                        email="sc-com@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_m_f)
    Club.objects.create(name="كلية طب الأسنان",
                        english_name="College of Dentistry",
                        description="-",
                        email="sc-cod@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R",
                        college=r_d_m)
    Club.objects.create(name="كلية طب الأسنان",
                        english_name="College of Dentistry",
                        description="-",
                        email="sc-codf@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_d_f)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="-",
                        email="sc-cams@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R",
                        college=r_a_m)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="-",
                        email="sc-camsf@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_a_f)
    Club.objects.create(name="كلية الصيدلة",
                        english_name="College of Pharmacy",
                        description="-",
                        email="sc-cop@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R",
                        college=r_p_m)
    Club.objects.create(name="كلية الصيدلة",
                        english_name="College of Pharmacy",
                        description="-",
                        email="sc-cop@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_p_f)
    Club.objects.create(name="كلية الصحة العامة والمعلوماتية الصحية",
                        english_name="College of Public Health and Health Informatics",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R",
                        college=r_i_m)
    Club.objects.create(name="كلية التمريض",
                        english_name="College of Nursing",
                        description="-",
                        email="sc-conr@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_n_f)
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="-",
                        email="arts.club@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="-",
                        email="arts.club@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="-",
                        email="bestnation.club@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="-",
                        email="bestnation.club@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي البحث والابتكار والتقنية",
                        english_name="Research, Innovation and Technology Club",
                        description="-",
                        email="researchclub@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي البحث والابتكار والتقنية",
                        english_name="Research, Innovation and Technology Club",
                        description="-",
                        email="researchclub@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="-",
                        email="LeenClub@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="-",
                        email="LeenClub@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="-",
                        email="arshidny@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="R")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidny",
                        description="-",
                        email="arshidny@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R")

    # Jeddah clubs
    # No female College of Medicine in Jeddah, yet. 
    Club.objects.create(name="كلية الطب",
                        english_name="College of Medicine",
                        description="-",
                        email="sc-comj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="J",
                        college=j_m_m)
    Club.objects.create(name="كلية التمريض",
                        english_name="College of Nursing",
                        description="-",
                        email="sc-conj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="J",
                        college=j_n_f)
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="-",
                        email="sc-coshpj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="J",
                        college=j_b_m)
    Club.objects.create(name="كلية العلوم و المهن الصحية",
                        english_name="College of Science and Health Professions",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="J",
                        college=j_b_f)
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="J")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="J")
    Club.objects.create(name="نادي البحث والابتكار والتقنية",
                        english_name="Research, Innovation and Technology Club",
                        description="-",
                        email="research.clubj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="J")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="J")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="J")

    # Al-Ahsa clubs
    Club.objects.create(name="كلية التمريض",
                        english_name="College of Nursing",
                        description="-",
                        email="sc-conah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="A",
                        college=a_n_f)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="-",
                        email="sc-cams@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="M",
                        year=year_2015_2016,
                        city="A",
                        college=a_a_m)
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="-",
                        email="sc-camsf@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="A",
                        college=a_a_f)
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="-",
                        email="arts.clubah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="A")
    Club.objects.create(name="نادي خير أمة",
                        english_name="Best Nation Club",
                        description="-",
                        email="bestnation.clubah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="A")
    Club.objects.create(name="نادي البحث والابتكار والتقنية",
                        english_name="Research, Innovation and Technology Club",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="A")
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="A")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="-",
                        email="pending@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2015_2016,
                        city="A")

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)

    Club.objects.get(english_name="Presidency (Jeddah)").delete()
    Club.objects.get(english_name="Presidency (Al-Ahsa)").delete()
    male_presidency = Club.objects.get(english_name="Presidency (Riyadh/Male)")
    male_presidency.name = "رئاسة نادي الطلاب (طلاب)"
    male_presidency.english_name = "Presidency (Male)"
    male_presidency.save()
    female_presidency = Club.objects.get(english_name="Presidency (Riyadh/Female)")
    male_presidency.name = "رئاسة نادي الطلاب (طالبات)"
    female_presidency.english_name = "Presidency (Female)"
    female_presidency.save()

    for club in Club.objects.filter(year=year_2015_2016):
        club.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0012_add_year_to_previous_clubs'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
