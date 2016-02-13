from django.db import models
from django.utils import timezone

from core.models import StudentClubYear


class ResearchHubQuerySet(models.QuerySet):
    def current_year(self):
        year = StudentClubYear.objects.get_current()
        return self.filter(year=year)

    def undeleted(self):
        return self.filter(is_deleted=False)

    # This works for both Supervisor and SkilledStudent models
    def available(self):
        now = timezone.now()
        return (self.filter(available_from__isnull=True,
                            available_until__isnull=True) | \
                self.filter(available_from__gte=now,
                            available_until__isnull=True) | \
                self.filter(available_from__isnull=True,
                            available_until__lte=now) | \
                self.filter(available_from__gte=now,
                            available_until__lte=now))\
                            .undeleted().filter(is_hidden=False)

    def unavailable(self):
        now = timezone.now()
        return self.undeleted().filter(is_hidden=True) | \
               self.undeleted().exclude(is_hidden=False,
                                        available_from__isnull=True,
                                        available_until__isnull=True)\
                               .exclude(is_hidden=False,
                                        available_from__gte=now,
                                        available_until__isnull=True)\
                               .exclude(is_hidden=False,
                                        available_from__isnull=True,
                                        available_until__lte=now)\
                               .exclude(is_hidden=False,
                                        available_from__gte=now,
                                        available_until__lte=now)

class ProjectQuerySet(ResearchHubQuerySet):
    def shown(self):
        return self.undeleted().filter(is_hidden=False)

    def hidden(self):
        return self.undeleted().filter(is_hidden=True)
