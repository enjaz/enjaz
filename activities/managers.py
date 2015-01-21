from django.db import models
from clubs.utils import get_presidency, get_deanship


class ActivityManager(models.Manager):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def approved(self):
        """
        Return a queryset of the current year's approved activities.
        """
        # Approved activities are those that have an approved presidency review
        # and an approved deanship review
        return self.filter(review__reviewer_club=get_presidency(),
                           review__is_approved=True)\
                   .filter(review__reviewer_club=get_deanship(),
                           review__is_approved=True)

    def pending(self):
        """
        Return a queryset of the current year's pending activities.
        """
        # Pending activities are those that are neither approved nor rejected.
        return self.filter(review__reviewer_club=get_presidency(), review__is_approved=None)\
                     .filter(review__reviewer_club=get_deanship(), review__is_approved=None)\
            | self.filter(review__reviewer_club=get_presidency(), review__is_approved=True)\
                    .filter(review__reviewer_club=get_deanship(), review__is_approved=None)\
            | self.filter(review__reviewer_club=get_presidency(), review__is_approved=None)\
                    .filter(review__reviewer_club=get_deanship(), review__is_approved=True)\
            | self.filter(review__reviewer_club=get_deanship())\
                    .exclude(review__reviewer_club=get_presidency(),).exclude(review__is_approved=False)\
            | self.filter(review__reviewer_club=get_presidency())\
                    .exclude(review__reviewer_club=get_deanship(),).exclude(review__is_approved=False)\
            | self.filter(review__isnull=True)

    def rejected(self):
        """
        Return a queryset of the current year's rejected activities.
        """
        # Rejected activities are those that have a rejected presidency review
        # or a rejected deanship review
        return self.filter(review__is_approved=False)