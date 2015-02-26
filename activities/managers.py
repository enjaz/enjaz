from django.db import models


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
        return self.filter(review__review_type="P",
                           review__is_approved=True)\
                   .filter(review__review_type="D",
                           review__is_approved=True)\
                   .filter(is_deleted=False)

    def pending(self):
        """
        Return a queryset of the current year's pending activities.
        """
        # Pending activities are those that are neither approved nor rejected.
        pending_activities = self.filter(review__review_type="P", review__is_approved=None).filter(review__review_type="D",
                                                                                     review__is_approved=None)\
            | self.filter(review__review_type="P", review__is_approved=True).filter(review__review_type="D",
                                                                                    review__is_approved=None)\
            | self.filter(review__review_type="P", review__is_approved=None).filter(review__review_type="D",
                                                                                    review__is_approved=True)\
            | self.filter(review__review_type="D").exclude(review__review_type=
                                                           "P").exclude(review__is_approved=False)\
            | self.filter(review__review_type="P").exclude(review__review_type=
                                                           "D").exclude(review__is_approved=False)\
            | self.filter(review__isnull=True)
        return pending_activities.filter(is_deleted=False)

    def rejected(self):
        """
        Return a queryset of the current year's rejected activities.
        """
        # Rejected activities are those that have a rejected presidency review
        # or a rejected deanship review
        return self.filter(review__is_approved=False, is_deleted=False)
