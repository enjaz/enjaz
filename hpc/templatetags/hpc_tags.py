from django import template

from hpc import utils


register = template.Library()

@register.filter
def is_research_committee_member(user):
    return utils.is_research_committee_member(user)

@register.filter
def is_organizing_committee_member(user):
    return utils.is_organizing_committee_member(user)
