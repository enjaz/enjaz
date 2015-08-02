from django.db import models
from core.models import StudentClubYear


current_year = StudentClubYear.objects.get_current()

class CodeQuerySet(models.QuerySet):
    def current_year(self):
        return self.filter(year=current_year)
