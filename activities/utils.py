"""
Utility functions for the activities app.
"""
from activities.models import Activity


def get_approved_activities():
    """
    Return a query set of the current year's approved activities.
    """
    # Approved activities are those who have an approved deanship review
    return Activity.objects.filter(review__review_type="D", review__is_approved=True)