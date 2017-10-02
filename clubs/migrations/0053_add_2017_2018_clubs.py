# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2017_2018 = StudentClubYear.objects.get(start_date__year=2017,
                                                 end_date__year=2018)

    # Deanship of Student Affairs
    riyadh_deanship = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year_2017_2018,
        email="studentsclub@ksau-hs.edu.sa",
        visible=False,
        can_review=True,
        can_view_assessments=False,
        is_assessed=False,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city=u"الرياض",
    )
    jeddah_deanship = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year_2017_2018,
        email="studentsclub@ksau-hs.edu.sa",
        parent=riyadh_deanship,
        visible=False,
        can_review=True,
        can_view_assessments=False,
        is_assessed=False,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city=u"جدة",
    )
    alahsa_deanship = Club.objects.create(
        name="عمادة شؤون الطلاب",
        english_name="Deanship of Student Affairs",
        description="",
        year=year_2017_2018,
        email="studentsclub@ksau-hs.edu.sa",
        parent=riyadh_deanship,
        visible=False,
        can_review=True,
        can_view_assessments=False,
        is_assessed=False,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city=u"الأحساء",
    )

    # Presidency
    presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                     year=year_2017_2018,
                                     english_name="Presidency",
                                     description="",
                                     email="studentsclub@ksau-hs.edu.sa",
                                     parent=riyadh_deanship,
                                     can_review=False,
                                     visible=False,
                                     is_assessed=False,
                                     city=u"الرياض")
    male_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                          year=year_2017_2018,
                                          english_name="Presidency",
                                          description="",
                                          email="sc-m@ksau-hs.edu.sa",
                                          parent=presidency,
                                          can_review=True,
                                          can_assess=True,
                                          visible=False,
                                          is_assessed=False,
                                          gender="M",
                                          city=u"الرياض")
    female_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                            year=year_2017_2018,
                                            english_name="Presidency",
                                            description="",
                                            email="sc-f@ksau-hs.edu.sa",
                                            parent=presidency,
                                            can_review=True,
                                            can_assess=True,
                                            visible=False,
                                            is_assessed=False,
                                            gender="F",
                                            city=u"الرياض")
    jeddah_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                            year=year_2017_2018,
                                            english_name="Presidency",
                                            description="",
                                            email="sc-j@ksau-hs.edu.sa",
                                            parent=jeddah_deanship,
                                            can_review=True,
                                            can_assess=True,
                                            visible=False,
                                            is_assessed=False,
                                            city=u"جدة")
    alahsa_presidency = Club.objects.create(name="رئاسة نادي الطلاب",
                                            year=year_2017_2018,
                                            english_name="Presidency",
                                            description="",
                                            email="sc-ah@ksau-hs.edu.sa",
                                            parent=alahsa_deanship,
                                            can_review=True,
                                            can_assess=True,
                                            visible=False,
                                            is_assessed=False,
                                            city=u"الأحساء")

    # Media center
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency,
        description="",
        year=year_2017_2018,
        email="sc-media@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        gender="M",
        city=u"الرياض")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency,
        description="",
        year=year_2017_2018,
        email="sc-media@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        gender="F",
        city=u"الرياض")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency,
        description="",
        year=year_2017_2018,
        email="sc-mediaj@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city=u"جدة")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency,
        description="",
        year=year_2017_2018,
        email="sc-mediaah@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        can_submit_activities=False,
        can_edit=False,
        can_delete=False,
        city=u"الأحساء")

    # Get colleges
    # (Variables are named: <city_code>_<college_code>_<gender_code>)

    # ## Riyadh ##
    # i) Male
    r_m_m = College.objects.get(name='M', section='NG', city=u"الرياض",  # TODO: Change to actual name!
                                gender='M')
    r_d_m = College.objects.get(name='D', section='NG', city=u"الرياض",
                                gender='M')
    r_p_m = College.objects.get(name='P', section='NG', city=u"الرياض",
                                gender='M')
    r_a_m = College.objects.get(name='A', section='NG', city=u"الرياض",
                                gender='M')
    r_i_m = College.objects.get(name='I', section='NG', city=u"الرياض",
                                gender='M')
    r_b_m = College.objects.get(name='B', section='NG', city=u"الرياض",
                                gender='M')

    # ii) Female
    r_m_f = College.objects.get(name='M', section='NG', city=u"الرياض",
                                gender='F')
    r_d_f = College.objects.get(name='D', section='NG', city=u"الرياض",
                                gender='F')
    r_p_f = College.objects.get(name='P', section='NG', city=u"الرياض",
                                gender='F')
    r_a_f = College.objects.get(name='A', section='NG', city=u"الرياض",
                                gender='F')
    r_b_f = College.objects.get(name='B', section='NG', city=u"الرياض",
                                gender='F')
    r_n_f = College.objects.get(name='N', section='NG', city=u"الرياض",
                                gender='F')

    # ## Jeddah ##
    j_m_m = College.objects.get(name='M', section='J', city=u"جدة",
                                gender='M')
    j_m_f = College.objects.get(name='M', section='J', city=u"جدة",
                                gender='M')
    j_n_f = College.objects.get(name='N', section='J', city=u"جدة",
                                gender='F')
    j_b_m = College.objects.get(name='B', section='J', city=u"جدة",
                                gender='M')
    j_b_f = College.objects.get(name='B', section='J', city=u"جدة",
                                gender='F')
    j_a_m = College.objects.get(name='A', section='J', city=u"جدة",
                                gender='M')
    j_a_f = College.objects.get(name='A', section='J', city=u"جدة",
                                gender='F')

    # ## Al-Ahsa ##
    a_a_m = College.objects.get(name='A', section='A', city=u"الأحساء",
                                gender='M')
    a_a_f = College.objects.get(name='A', section='A', city=u"الأحساء",
                                gender='F')
    a_n_f = College.objects.get(name='N', section='A', city=u"الأحساء",
                                gender='F')

    # Riyadh clubs

    # ** 1) College clubs and deanships **
    colleges = [
        {
            'ar_name': u"كلية العلوم و المهن الصحية",
            'en_name': "College of Science and Health Professions",
            'sections': [r_b_m, r_b_f],
            'club_emails': {
                'M': 'sc-coshp@ksau-hs.edu.sa',
                'F': 'sc-coshpf@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية الطب",
            'en_name': "College of Medicine",
            'sections': [r_m_m, r_m_f],
            'club_emails': {
                'M': 'sc-com@ksau-hs.edu.sa',
                'F': 'sc-comf@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية العلوم الطبية التطبيقية",
            'en_name': "College of Applied Medical Sciences",
            'sections': [r_a_m, r_a_f],
            'club_emails': {
                'M': 'sc-cams@ksau-hs.edu.sa',
                'F': 'sc-cams-f@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية الصيدلة",
            'en_name': "College of Pharmacy",
            'sections': [r_p_m, r_p_f],
            'club_emails': {
                'M': 'sc-cop@ksau-hs.edu.sa',
                'F': 'sc-cop-f@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية طب الأسنان",
            'en_name': "College of Dentistry",
            'sections': [r_d_m, r_d_f],
            'club_emails': {
                'M': 'sc-cod@ksau-hs.edu.sa',
                'F': 'sc-codf@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية التمريض",
            'en_name': "College of Nursing",
            'sections': [r_n_f],
            'club_emails': {
                'F': 'sc-conr@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية الصحة العامة و المعلوماتية الصحية",
            'en_name': "College of Public Health and Health Informatics",
            'sections': [r_i_m],
            'club_emails': {
                'M': 'sc-cphhi@ksau-hs.edu.sa',
            }
        },
    ]
    for college in colleges:
        for section in college['sections']:
            college_deanship = Club.objects.create(
                name=u"عمادة {}".format(college['ar_name']),
                english_name="Deanship of the {}".format(college['en_name']),
                description="",
                email="pending@ksau-hs.edu.sa",
                parent=female_presidency if section.gender == 'F' else male_presidency,
                gender=section.gender,
                city=u"الرياض",
                year=year_2017_2018,
                visible=False,
                can_review=True,
                can_delete=False,
                can_edit=False
            )
            Club.objects.create(
                name=college['ar_name'],
                english_name=college['en_name'],
                description="",
                email=college['club_emails'][section.gender],
                parent=college_deanship,
                gender=section.gender,
                year=year_2017_2018,
                city=u"الرياض",
                college=section,
            )

    # ** 2) Specialized clubs **
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي بصيرة",
                        english_name="Baseerah Club",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي بصيرة",
                        english_name="Baseerah Club",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي لين",
                        english_name="Leen Club",
                        description="",
                        email="LeenClub@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="نادي لين",
                        english_name="Leen Club",
                        description="",
                        email="LeenClub@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"الرياض")

    # ** 3) Initiatives **
    Club.objects.create(name="أرشدني",
                        english_name="Arshidny",
                        description="",
                        email="arshidny@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="أرشدني",
                        english_name="Arshidny",
                        description="",
                        email="arshidny@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="سراج",
                        english_name="Siraj",
                        description="",
                        email="siraj@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="سراج",
                        english_name="Siraj",
                        description="",
                        email="siraj@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"الرياض")
    Club.objects.create(name="ResearchHub",
                        english_name="ResearchHub",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=male_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"الرياض")

    # Jeddah clubs
    # ** 1) College deanships and clubs **

    jed_colleges = [
        {
            'ar_name': u"كلية العلوم و المهن الصحية",
            'en_name': "College of Science and Health Professions",
            'sections': [j_b_m, j_b_f],
            'club_emails': {
                'M': 'sc-coshpj@ksau-hs.edu.sa',
                'F': 'sc-coshpfj@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية الطب",
            'en_name': "College of Medicine",
            'sections': [j_m_m, j_m_f],
            'club_emails': {
                'M': 'sc-comj@ksau-hs.edu.sa',
                'F': 'sc-comfj@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية العلوم الطبية التطبيقية",
            'en_name': "College of Applied Medical Sciences",
            'sections': [j_a_m, j_a_f],
            'club_emails': {
                'M': 'pending@ksau-hs.edu.sa',
                'F': 'sc-camsfj@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية التمريض",
            'en_name': "College of Nursing",
            'sections': [j_n_f],
            'club_emails': {
                'F': 'sc-conj@ksau-hs.edu.sa',
            }
        },
    ]
    jed_deanships = {
        'M': [],
        'F': [],
    }
    for college in jed_colleges:
        for section in college['sections']:
            college_deanship = Club.objects.create(
                name=u"عمادة {}".format(college['ar_name']),
                english_name="Deanship of the {}".format(college['en_name']),
                description="",
                email="pending@ksau-hs.edu.sa",
                parent=jeddah_presidency,
                gender=section.gender,
                city=u"جدة",
                year=year_2017_2018,
                visible=False,
                can_review=True,
                can_delete=False,
                can_edit=False
            )
            jed_deanships[section.gender].append(college_deanship)
            Club.objects.create(
                name=college['ar_name'],
                english_name=college['en_name'],
                description="",
                email=college['club_emails'][section.gender],
                parent=college_deanship,
                gender=section.gender,
                year=year_2017_2018,
                city=u"جدة",
                college=section,
            )

    # ** 2) Specialized clubs **
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['M'])
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.club-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['F'])
    Club.objects.create(name="نادي بصيرة",
                        english_name="Baseerah Club",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['M'])
    Club.objects.create(name="نادي بصيرة",
                        english_name="Baseerah Club",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['F'])
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['M'])
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['F'])
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="leenclub-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['M'])
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="leenclub-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['F'])

    # ** 3) Initiatives **
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="",
                        email="arshidny-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="M",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['M'])
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="",
                        email="arshidny-j@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="F",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*jed_deanships['F'])
    Club.objects.create(name="سراج",
                        english_name="Siraj",
                        description="",
                        email="siraj@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"جدة").possible_parents.add(*(jed_deanships['M'] + jed_deanships['M']))

    # Al-Ahsa clubs
    # ** 1) College deanships and clubs **

    ahsa_colleges = [
        {
            'ar_name': u"كلية العلوم الطبية التطبيقية",
            'en_name': "College of Applied Medical Sciences",
            'sections': [a_a_m, a_a_f],
            'club_emails': {
                'M': 'sc-cams-ah@ksau-hs.edu.sa',
                'F': 'sc-camsf-ah@ksau-hs.edu.sa',
            }
        },
        {
            'ar_name': u"كلية التمريض",
            'en_name': "College of Nursing",
            'sections': [a_n_f],
            'club_emails': {
                'F': 'sc-conah@ksau-hs.edu.sa',
            }
        },
    ]
    ahsa_deanships = []
    for college in ahsa_colleges:
        for section in college['sections']:
            college_deanship = Club.objects.create(
                name=u"عمادة {}".format(college['ar_name']),
                english_name="Deanship of the {}".format(college['en_name']),
                description="",
                email="pending@ksau-hs.edu.sa",
                parent=alahsa_presidency,
                gender=section.gender,
                city=u"الأحساء",
                year=year_2017_2018,
                visible=False,
                can_review=True,
                can_delete=False,
                can_edit=False
            )
            ahsa_deanships.append(college_deanship)
            Club.objects.create(
                name=college['ar_name'],
                english_name=college['en_name'],
                description="",
                email=college['club_emails'][section.gender],
                parent=college_deanship,
                gender=section.gender,
                year=year_2017_2018,
                city=u"الأحساء",
                college=section,
            )

    # ** 2) Specialized clubs **
    Club.objects.create(name="نادي الفنون",
                        english_name="Arts Club",
                        description="",
                        email="arts.clubah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"الأحساء").possible_parents.add(*ahsa_deanships)
    Club.objects.create(name="نادي بصيرة",
                        english_name="Baseerah Club",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"الأحساء").possible_parents.add(*ahsa_deanships)
    Club.objects.create(name="نادي مشكاة",
                        english_name="Mishkat Club",
                        description="",
                        email="mishkatclub-ah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"الأحساء").possible_parents.add(*ahsa_deanships)
    Club.objects.create(name="نادي لين التطوعي",
                        english_name="Leen Club",
                        description="",
                        email="leenclub.ah@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"الأحساء").possible_parents.add(*ahsa_deanships)

    # ** 3) Initiatives **
    Club.objects.create(name="أرشدني",
                        english_name="Arshidni",
                        description="",
                        email="arshidny-a@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"الأحساء").possible_parents.add(*ahsa_deanships)
    Club.objects.create(name="سراج",
                        english_name="Siraj",
                        description="",
                        email="siraj@ksau-hs.edu.sa",
                        parent=alahsa_presidency,
                        gender="",
                        year=year_2017_2018,
                        city=u"الأحساء").possible_parents.add(*ahsa_deanships)


def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2017_2018 = StudentClubYear.objects.get(start_date__year=2017,
                                                 end_date__year=2018)

    Club.objects.filter(year=year_2017_2018).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0052_presidencies_can_assess'),
        ('core', '0013_add_2017_2018_year'),
    ]

    operations = [
        migrations.RunPython(
            add_clubs,
            remove_clubs,
        )
    ]
