# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fill_new_fields(apps, schema_editor):
    Code = apps.get_model('niqati', 'Code')
    Code_Order = apps.get_model('niqati', 'Code_Order')
    Review = apps.get_model('niqati', 'Review')
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2014_2015 = StudentClubYear.objects.get(start_date__year=2014,
                                                 end_date__year=2015)
    presidency = Club.objects.get(english_name="Presidency",
                                  year=year_2014_2015)

    # Only apply this to old-style code (useful if this migrations was
    # ever to be applied in later years).
    for code in Code.objects.filter(year=None, points=0):
        code.year = year_2014_2015
        code.points = code.category.points
        if code.asset.startswith("http"):
            code.short_link = code.asset
        code.save()

    reviews = []
    for order in Code_Order.objects.filter(code_collection__approved__in=[True, False]).distinct():
        is_approved = order.code_collection_set.first().approved
        review = Review(order=order,
                        reviewer_club=presidency,
                        is_approved=is_approved)

    Review.objects.bulk_create(reviews)

def empty_new_fields(apps, schema_editor):
    Code = apps.get_model('niqati', 'Code')
    Code_Order = apps.get_model('niqati', 'Code_Order')
    Review = apps.get_model('niqati', 'Review')
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2014_2015 = StudentClubYear.objects.get(start_date__year=2014,
                                                 end_date__year=2015)
    presidency = Club.objects.get(english_name="Presidency",
                                  year=year_2014_2015)

    for code in Code.objects.filter(year=year_2014_2015):
        code.year = None
        code.points = 0
        if code.short_link:
            code.asset = code.short_link
            code.short_link = ""
        code.save()

    for review in Review.objects.filter(reviewer_club=presidency):
        review.order.code_collection_set.update(approved=review.is_approved)
        review.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0005_auto_20150729_0727'),
    ]

    operations = [
       migrations.RunPython(
           fill_new_fields,
           reverse_code=empty_new_fields)
    ]
