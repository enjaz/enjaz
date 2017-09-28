from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone


class StudentClubYearManager(models.Manager):
    def get_by_year(self, start_year, end_year):
        return self.get(start_date__year=start_year,
                        end_date__year=end_year)

    def get_current(self):
        now = timezone.now()
        try:
            return self.get(start_date__lte=now, end_date__gte=now)
        except ObjectDoesNotExist:
            return self.order_by('end_date').last()