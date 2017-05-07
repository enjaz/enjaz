from django import template
from certificates import utils

register = template.Library()

@register.filter
def certificate_has_surveys(user):
    return utils.certificate_has_surveys(user)
