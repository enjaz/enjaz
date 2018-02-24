from django import template

from matching_program import utils


register = template.Library()

@register.filter
def is_matchingProgram_coordinator_or_member(user):
    return utils.is_matchingProgram_coordinator_or_member(user)



