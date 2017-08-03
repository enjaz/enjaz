from django.db.models.signals import post_save
from django.dispatch import receiver

from approvals.models import ActivityRequest


@receiver(post_save, sender=ActivityRequest)
def notify_reviewers_of_new_request(sender, **kwargs):
    """
    If the activity request is newly created, send a notification to reviewers.
    """
    pass  # TODO
