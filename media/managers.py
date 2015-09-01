from django.db import models
from django.utils import timezone

from clubs.models import Club

class PollManager(models.Manager):
    """
    A custom manager for polls.
    """
    def hundred_says(self):
        return self.filter(poll_type=HUNDRED_SAYS)

    def what_if(self):
        return self.filter(poll_type=WHAT_IF)

    def active(self):
        """
        Return objects whose open date is before or equal to now, and whose close date is still ahead.
        """
        return self.filter(open_date__lte=timezone.now(), close_date__gt=timezone.now())

    def past(self):
        """
        Return objects whose close date is before ``now``.
        """
        return self.filter(close_date__lte=timezone.now())

    def upcoming(self):
        """
        Return objects whose open date is to come yet.
        """
        return self.filter(open_date__gt=timezone.now())

class BuzzManager(models.Manager):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def published(self):
        """
        Return objects whose open date is before or equal to now, and whose close date is still ahead.
        """
        return self.filter(announcement_date__lte=timezone.now(), is_deleted=False).order_by('-announcement_date')

    def upcoming(self):
        """
        Return objects whose open date is to come yet.
        """
        return self.filter(announcement_date__gt=timezone.now(), is_deleted=False).order_by('-announcement_date')

class FollowUpQuerySet(models.QuerySet):
    def current_year(self):
        return self.filter(episode__activity__primary_club__in=Club.objects.current_year()).distinct()

