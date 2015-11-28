from django import template

from studentguide import utils

register = template.Library()

@register.filter
def is_studentguide_member(user):
    return utils.is_studentguide_member(user)

@register.filter
def is_studentguide_coordinator_or_deputy(user):
    return utils.is_studentguide_coordinator_or_deputy(user)

@register.filter
def has_guide_profile(user):
    return utils.has_guide_profile(user)

@register.filter
def has_pending_requests(user):
    return user.guide_profiles.current_year().first().guide_requests.pending().exists()

@register.filter
def can_edit_guide(user, guide):
    return utils.can_edit_guide(user, guide)

@register.filter
def can_add_request(user, guide):
    return utils.can_add_request(user, guide)

@register.filter
def has_current_guide_profile(user):
    return user.guide_profiles.current_year().exists()

@register.filter
def is_guide_of_user(guide, user):
    return utils.is_guide_of_user(guide, user)

@register.filter
def has_pending_request(user, guide):
    return utils.has_pending_request(user, guide)
