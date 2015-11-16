
# -*- coding: utf-8  -*-
from django.db import models

from accounts.utils import get_user_city, get_user_gender
from core.models import StudentClubYear

class RequestQuerySet(models.QuerySet):
    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(guide__year=current_year)

    def pending(self):
        return self.filter(guide_status='P', requester_status='A')

    def canceled(self):
        return self.filter(guide_status='R') | \
               self.filter(requester_status='C')

    def accepted(self):
        return self.filter(guide_status='A', requester_status='A')

class GuideQuerySet(models.QuerySet):
    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(year=current_year)

    def available(self):
        return self.filter(is_available=True)

    def unavailable(self):
        return self.filter(is_available=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def undeleted(self):
        return self.filter(is_deleted=False)

    def for_user_gender(self, user=None):
        gender_condition = models.Q()

        if user:
            gender = get_user_gender(user)
            if gender:
                gender_condition = models.Q(user__common_profile__college__gender=gender)

        return self.filter(gender_condition)

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user:
            city = get_user_city(user)
            if city:
                city_condition = models.Q(user__common_profile__city=city)

        return self.filter(city_condition)

class ReportQuerySet(models.QuerySet):
    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(guide__year=current_year)
    def undeleted(self):
        return self.filter(is_deleted=False)

class FeedbackQuerySet(models.QuerySet):
    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(guide__year=current_year)

