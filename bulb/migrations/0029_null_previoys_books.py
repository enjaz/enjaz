# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def mark_was_announced_null(apps, schema_editor):
    Book = apps.get_model('bulb', 'Book')
    cities = ["الرياض", "جدة", "الأحساء"]
    for city in cities:
        last_four = Book.objects.filter(submitter__common_profile__city=city)\
                                .order_by("-submission_date")[:4]\
                                .values_list("pk", flat=True)
        # WebFaction version of MySQL is a little bit old fashioned
        # that we have to do the following one line:
        last_four = list(last_four)
        Book.objects.filter(submitter__common_profile__city=city)\
                    .exclude(pk__in=last_four)\
                    .order_by("-submission_date")\
                    .update(was_announced=None)

def mark_was_announced_false(apps, schema_editor):
    Book = apps.get_model('bulb', 'Book')
    Book.objects.update(was_announced=False)

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0028_twitter_annoucement_fields'),
    ]

    operations = [
       migrations.RunPython(
            mark_was_announced_null,
            reverse_code=mark_was_announced_false),
    ]
