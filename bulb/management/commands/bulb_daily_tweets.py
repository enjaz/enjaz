# -*- coding: utf-8  -*-
import locale
import os
import subprocess

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils import timezone 
from bulb.models import Book
from core.utils import create_tweet_by_access

class Command(BaseCommand):
    help = "Send a tweet on latest books."
    def add_arguments(self, parser):
        parser.add_argument('--city', dest='city_code',
                            type=str)

    def handle(self, *args, **options):
        cities = {'R': u'الرياض',
                  'J': u'جدة',
                  'A': u'الأحساء'}
        domain = Site.objects.get_current().domain
        full_url = "https://{}{}".format(domain,
                                         reverse('bulb:index'))
        city_code = options['city_code']
        city = cities[city_code] 
        locale.setlocale(locale.LC_ALL,'ar_EG.utf8')
        today = timezone.now().date()
        day_string = today.strftime(u'%A %-d %B %Y').decode("utf-8")
        directory = os.path.join(settings.MEDIA_ROOT, "bulb_channel/")
        covers = []
        targetted_books = Book.objects.current_year().available()\
                                      .undeleted()\
                                      .order_by("submission_date")\
                                      .filter(submitter__common_profile__city=city,
                                              was_announced=False)

        # Don't continue if we have less than two covers to report
        if targetted_books.count() < 2:
            return

        for book in targetted_books[:4]:
            covers.append(book.cover.path)
            book.was_announced = True
            book.save()

        collection_photo = directory + today.strftime("%Y%m%d-{}.jpg".format(city_code))
        subprocess.call(u"montage -geometry 200x300>+10+10 {} {}".format(u" ".join(covers), collection_photo), shell=True)
        create_tweet_by_access("bulb", u"{} | آخر الكتب التي أضافتها الطالبات والطلاب ليوم {}!\n{} #مبادرة_سِراج".format(city, day_string, full_url), collection_photo)
