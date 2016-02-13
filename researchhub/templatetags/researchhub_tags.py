from django import template

from researchhub import utils


register = template.Library()

@register.filter
def has_current_skill_profile(user):
    return user.researchhub_skill_profiles.current_year().exists()

@register.filter
def is_researchhub_coordinator_or_member(user):
    return utils.is_researchhub_coordinator_or_member(user)

@register.filter
def can_edit_project(user, project):
    return utils.can_edit_project(user, project)

@register.filter
def can_edit_skill(user, skill):
    return utils.can_edit_skill(user, skill)

@register.filter
def can_edit_supervisor(user, supervisor):
    return utils.can_edit_supervisor(user, supervisor)
