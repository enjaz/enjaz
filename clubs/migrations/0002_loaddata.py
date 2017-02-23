# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

def load_default_clubs(apps, shema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')

    # If Presidency exists as a Club, we can be faily sure that the
    # database already contains data and we shouldn't import our clubs
    # again.
    if Club.objects.filter(english_name="Presidency"):
        return

    ng_male_medicine = College.objects.create(
      city="الرياض",
      section="NG", 
      name="M", 
      gender="M"
    )

    ng_male_pharmacy = College.objects.create(
      city="الرياض",
      section="NG", 
      name="P", 
      gender="M"
    )

    ng_male_dentistry = College.objects.create(
      city="الرياض",
      section="NG", 
      name="D", 
      gender="M"
    )

    ng_male_basic = College.objects.create(
      city="الرياض",
      section="NG", 
      name="B", 
      gender="M"
    )

    ng_male_applied = College.objects.create(
      city="الرياض",
      section="NG", 
      name="A", 
      gender="M"
    )

    ng_female_medicine = College.objects.create(
      city="الرياض",
      section="NG", 
      name="M", 
      gender="F"
    )

    ng_female_nursing = College.objects.create(
      city="الرياض",
      section="NG", 
      name="N", 
      gender="F"
    )

    kfmc_male_medicine = College.objects.create(
      city="الرياض",
      section="KF", 
      name="M", 
      gender="M"
    )

    ng_female_basic = College.objects.create(
      city="الرياض",
      section="NG", 
      name="B", 
      gender="F"
    )

    ng_female_dentistry = College.objects.create(
      city="الرياض",
      section="NG", 
      name="D", 
      gender="F"
    )

    Club.objects.create(
      city="", 
      name="\u0631\u0626\u0627\u0633\u0629 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628", 
      english_name="Presidency", 
      email="studentsclub@ksua-hs.edu.sa", 
      description="\u0631\u0626\u0627\u0633\u0629 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0627\u0644\u0645\u0631\u0643\u0632 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a", 
      english_name="Media Center", 
      email="sc-media@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="", 
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0648 \u0627\u0644\u0645\u0647\u0646 \u0627\u0644\u0635\u062d\u064a\u0629 - \u0637\u0644\u0627\u0628", 
      college=ng_male_basic, 
      english_name="College of Science and Health Professions - Male", 
      email="sc-coshp@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="", 
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0648 \u0627\u0644\u0645\u0647\u0646 \u0627\u0644\u0635\u062d\u064a\u0629 - \u0637\u0627\u0644\u0628\u0627\u062a", 
      college=ng_female_basic, 
      english_name="College of Science and Health Professions - Female", 
      email="sc-coshpf@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628 - \u0637\u0644\u0627\u0628", 
      college=ng_male_medicine, 
      english_name="College of Medicine - Male", 
      email="sc-com@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="", 
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628 - \u0637\u0627\u0644\u0628\u0627\u062a", 
      college=ng_female_medicine, 
      english_name="College of Medicine - Female", 
      email="sc-comf@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0643\u0644\u064a\u0629 \u0637\u0628 \u0627\u0644\u0623\u0633\u0646\u0627\u0646 - \u0637\u0644\u0627\u0628", 
      college=ng_male_dentistry, 
      english_name="College of Dentistry - Male", 
      email="sc-cod@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="", 
      name="\u0643\u0644\u064a\u0629 \u0637\u0628 \u0627\u0644\u0623\u0633\u0646\u0627\u0646 - \u0637\u0627\u0644\u0628\u0627\u062a", 
      college=ng_female_dentistry, 
      english_name="College of Dentistry - Female", 
      email="sc-codf@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="", 
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u064a\u0629", 
      college=ng_male_applied, 
      english_name="College of Applied Medical Sciences", 
      email="sc-cams@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u0635\u064a\u062f\u0644\u0629", 
      college=ng_male_pharmacy, 
      english_name="College of Pharmacy", 
      email="sc-cop@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0643\u0644\u064a\u0629 \u0627\u0644\u062a\u0645\u0631\u064a\u0636", 
      college=ng_female_nursing, 
      english_name="College of Nursing", 
      email="sc-conr@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0646\u0627\u062f\u064a \u0627\u0644\u0642\u0631\u0627\u0621\u0629", 
      english_name="Reading Club", 
      email="reading.club@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0646\u0627\u062f\u064a \u0627\u0644\u062a\u0635\u0648\u064a\u0631 \u0627\u0644\u0641\u0648\u062a\u0648\u063a\u0631\u0627\u0641\u064a", 
      english_name="Photography Club", 
      email="photo.club@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0646\u0627\u062f\u064a \u0627\u0644\u0628\u062d\u062b \u0627\u0644\u0639\u0644\u0645\u064a", 
      english_name="Research Club", 
      email="research.club@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0646\u0627\u062f\u064a \u062e\u064a\u0631 \u0623\u0645\u0629", 
      english_name="Best Nation Club", 
      email="bestnation.club@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0646\u0627\u062f\u064a \u0627\u0644\u0641\u0646\u0648\u0646", 
      english_name="Arts Club", 
      email="arts.club@ksau-hs.edu.sa", 
      description="-"
    )
    
    Club.objects.create(
      city="الرياض",
      name="\u0646\u0627\u062f\u064a \u0627\u0644\u062d\u0648\u0627\u0633\u064a\u0628", 
      english_name="Computers Club", 
      email="computers.club@ksau-hs.edu.sa", 
      description="-"
    )



class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(
            load_default_clubs)
    ]
