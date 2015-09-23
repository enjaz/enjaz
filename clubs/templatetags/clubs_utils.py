from django import template
from clubs import utils as club_utils
from activities import utils as activity_utils
from clubs.models import Club

register = template.Library()

# NOTE that in filters that take 2 arguments, the arguments of the filter are the opposite of the util function
# (in terms of order)

@register.filter
def is_coordinator_of_any_club(user):
    return club_utils.is_coordinator_of_any_club(user)

@register.filter
def is_member_of_any_club(user):
    return club_utils.is_member_of_any_club(user)

@register.filter
def is_employee_of_any_club(user):
    return club_utils.is_employee_of_any_club(user)

@register.filter
def is_coordinator(user, club):
    return club_utils.is_coordinator(club, user)

@register.filter
def is_deputy(user, club):
    return club_utils.is_deputy(club, user)

@register.filter
def is_member(user, club):
    return club_utils.is_member(club, user)

@register.filter
def is_coordinator_or_member(user, club):
    return club_utils.is_coordinator_or_member(club, user)

@register.filter
def is_coordinator_or_deputy(user, club):
    return club_utils.is_coordinator_or_deputy(club, user)

@register.filter
def is_employee(user, club):
    return club_utils.is_employee(club, user)

@register.filter
def has_coordination_to_activity(user, activity):
    return club_utils.has_coordination_to_activity(user, activity)

@register.filter
def can_review_activity(user, activity):
    return club_utils.can_review_activity(user, activity)

@register.filter
def can_delete_activity(user, activity):
    return club_utils.can_delete_activity(user, activity)

@register.filter
def can_edit_activity(user, activity):
    return club_utils.can_edit_activity(user, activity)

@register.filter
def can_assess_club(user, club):
    return activity_utils.can_assess_club(user, club)

@register.filter
def can_view_assessments(user, club):
    return activity_utils.can_view_assessments(user, club)

@register.filter
def get_activity_reviewing_parents(activity):
    return Club.objects.activity_reviewing_parents(activity)

@register.filter
def can_review_any_niqati(user):
    return club_utils.can_review_any_niqati(user)

@register.filter
def can_assess_any_club(user):
    return activity_utils.can_assess_any_club(user)

@register.filter
def can_submit_activities(user):
    return club_utils.can_submit_activities(user)
