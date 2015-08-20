from django.db import models

from accounts.utils import get_user_city, get_user_gender
from core.models import StudentClubYear


class ColleagueQuerySet(models.QuerySet):
    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(year=current_year)

    def available(self):
        return self.filter(is_available=True)

    def published(self):
        return self.filter(is_published=True)

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
