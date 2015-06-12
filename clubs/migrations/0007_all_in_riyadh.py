# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def make_all_in_riyadh(apps, schema_edtior):
    """For all previous clubs with no city, let's assume all of them are
       from Riyadh."""
    Club = apps.get_model('clubs', 'Club')
    for club in Club.objects.filter(city=""):
        club.city = "R"
        club.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_manytomany_not_null'),
    ]

    operations = [
       migrations.RunPython(
            make_all_in_riyadh),

    ]
