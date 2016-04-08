# -*- coding: utf-8  -*-
import datetime

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from post_office import mail

class Command(BaseCommand):
    help = "Email thsoe who didn't have an initial borrowing balance."

    def handle(self, *args, **options):
        for user in User.objects.filter(is_active=True,
                            common_profile__is_student=True,
                            book_points__category='L',
                            book_points__note=u"رصيد مبدئي",
                            book_points__submission_date__gte=datetime.datetime(2016,2,26),
                            book_points__submission_date__lt=datetime.datetime(2016,2,27)):
            print "Emailing", user.username
            try:
                mail.send([user.email],
                          template="bulb_added_point",
                          context={'user': user})
            except ValidationError:
                pass
