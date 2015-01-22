from django.db import models
from django.db.models.aggregates import Count


class ActivityManager(models.Manager):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def get_queryset(self):
        """
        TODO: Exclude delete activities.
        TODO: Exclude but the current year's activities.
        """
        return super(ActivityManager, self).get_queryset()

    def approved(self):
        """
        Return a queryset of approved activities.
        """
        # An approved activity is one which:
        # (1) has a number of reviews equal to the number of its reviewer parents
        # (2) has all of its reviews approved

        # The following is dirty way of dealing with query sets, but this is the only way given the deep complexity
        # of this query

        # WARNING: lengthy run-time; not lazy

        activities = self.all()
        approved_activities = filter(lambda activity: activity.is_approved(), activities)
        approved_pks = [activity.pk for activity in approved_activities]

        return self.filter(pk__in=approved_pks)

    def rejected(self):
        """
        Return a queryset of rejected activities.
        """
        # A rejected activity is one which:
        # (1) has at least 1 review
        # (2) has any of its reviews rejected
        return self.annotate(review_count=Count("review")).filter(review_count__gte=1, review__is_approved=False)

    def pending(self):
        """
        Return a queryset of pending activities.
        """
        # A pending activity is one that's not approved or rejected

        # The following is dirty way of dealing with query sets, but this is the only way given the deep complexity
        # of this query

        # WARNING: lengthy run-time; not lazy

        pending_activities = filter(lambda activity: activity.is_approved() is None, self.all())
        pending_pks = [activity.pk for activity in pending_activities]

        return self.filter(pk__in=pending_pks)
