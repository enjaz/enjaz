from django import template

from events import utils


register = template.Library()

@register.filter
def is_organizing_committee_member(event, user):
    return utils.is_organizing_committee_member(event, user)
