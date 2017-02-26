# -*- coding: utf-8  -*-
import locale
import os
import subprocess

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone 
from bulb.models import Book
from core.utils import create_tweet_by_access

class Command(BaseCommand):
    help = "Send a tweet on latest books."

    def handle(self, *args, **options):
        locale.setlocale(locale.LC_ALL,'ar_EG.utf8')
        today = timezone.now().date()
        day_string = today.strftime(u'%A %-d %B %Y').decode("utf-8")
        directory = os.path.join(settings.MEDIA_ROOT, "bulb_channel/")
        cities = [('R', u'الرياض'),
                  ('J', u'جدة'),
                  ('A', u'الأحساء')]
        for city_code, city in cities:
            covers = []
            for book in Book.objects.current_year().available().undeleted()\
                                                   .order_by("-submission_date")\
                                                   .filter(submitter__common_profile__city=city,
                                                           was_announced=False)[:4]:
                covers.append(book.cover.path)

            if not covers:
                continue
            collection_photo = directory + today.strftime("%Y%m%d-{}.jpg".format(city_code))
            subprocess.call(u"montage -geometry 200x300>+10+10 {} {}".format(u" ".join(covers), collection_photo), shell=True)
            create_tweet_by_access("bulb", u"{} | آخر الكتب التي أضافتها الطالبات والطلاب ليوم {}!\n#مبادرة_سِراج".format(city, day_string), collection_photo)
