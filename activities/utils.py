"""
Utility functions for the activities app.
"""
from activities.models import Activity
from clubs.utils import is_coordinator


def get_approved_activities():
    """
    Return a queryset of the current year's approved activities.
    """
    # Approved activities are those that have an approved presidency review
    # and an approved deanship review
    # return Activity.objects.filter(approved_by_d, approved_by_p)
    return Activity.objects.filter(review__review_type="P",
                                   review__is_approved=True)\
                           .filter(review__review_type="D",
                                   review__is_approved=True)


def get_rejected_activities():
    """
    Return a queryset of the current year's rejected activities.
    """
    # Rejected activities are those that have a rejected presidency review
    # or a rejected deanship review
    return Activity.objects.filter(review__is_approved=False)


def get_pending_activities():
    """
    Return a queryset of the current year's pending activities.
    """
    # Pending activities are those that are neither approved nor rejected.
    return Activity.objects.filter(review__review_type="P", review__is_approved=None).filter(review__review_type="D",
                                                                                             review__is_approved=None)\
        |  Activity.objects.filter(review__review_type="P", review__is_approved=True).filter(review__review_type="D",
                                                                                             review__is_approved=None)\
        |  Activity.objects.filter(review__review_type="P", review__is_approved=None).filter(review__review_type="D",
                                                                                             review__is_approved=True)\
        |  Activity.objects.filter(review__review_type="D").exclude(review__review_type=
                                                                    "P").exclude(review__is_approved=False)\
        |  Activity.objects.filter(review__review_type="P").exclude(review__review_type=
                                                                    "D").exclude(review__is_approved=False)\
        |  Activity.objects.filter(review__isnull=True)


def has_submitted_any_activity(user):
    """Return whether the user has ever submitted any activities."""
    return Activity.objects.filter(submitter__pk=user.pk).exists()


def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for activities."""
    # Confirm that the passed object is an ``Activity`` instance
    if not isinstance(object, Activity):
        raise TypeError("Expected an Activity object, received %s" % type(object))
    return is_coordinator(object.primary_club, user) or user.is_superuser