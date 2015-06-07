# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def get_presidency_and_deanship(apps):
    Club = apps.get_model('clubs', 'Club')
    presidency = Club.objects.get(english_name="Presidency")
    deanship = Club.objects.get(english_name="Deanship of Student Affairs")
    return presidency, deanship

def upgrade_reviews(apps, schema_editor):
    presidency, deanship = get_presidency_and_deanship(apps)
    Review = apps.get_model('activities', 'Review')
    Review.objects.filter(review_type="P").update(reviewer_club=presidency)
    Review.objects.filter(review_type="D").update(reviewer_club=deanship)

def downgrade_reviews(apps, schema_editor):
    presidency, deanship = get_presidency_and_deanship(apps)
    Review = apps.get_model('activities', 'Review')
    Review.objects.filter(reviewer_club=presidency).update(review_type="P")
    Review.objects.filter(reviewer_club=deanship).update(review_type="D")
    Review.objects.update(reviewer_club=None)

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_review_reviewer_club'),
        ('clubs', '0004_add_dsa'),
    ]

    operations = [
       migrations.RunPython(
            upgrade_reviews,
            reverse_code=downgrade_reviews),
    ]
