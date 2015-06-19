from django.db import models
from accounts.utils import get_user_city, get_user_gender
from core.models import StudentClubYear

current_year = StudentClubYear.objects.get_current()

class ClubQuerySet(models.QuerySet):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def visible(self):
        return self.filter(visible=True)

    def current_year(self):
        return self.filter(models.Q(year=current_year) | models.Q(year__isnull=True))

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user:
            city = get_user_city(user)
            if city:
                city_condition = models.Q(city=city) | \
                                 models.Q(city="")
        return self.filter(city_condition)

    def for_user_gender(self, user=None):
        gender_condition = models.Q()

        if user:
            gender = get_user_gender(user)
            if gender:
                gender_condition = models.Q(gender=gender) | \
                                   models.Q(gender="")
        return self.filter(gender_condition)
