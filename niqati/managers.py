from django.db import models
from core.models import StudentClubYear

class CodeQuerySet(models.QuerySet):
    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(year=current_year)
