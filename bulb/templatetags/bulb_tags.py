from django import template
from bulb import utils

from media.models import RED, GREEN, BLUE, AERO, GREY, ORANGE, YELLOW, PINK, PURPLE

register = template.Library()

@register.filter
def is_bulb_coordinator_or_deputy(user):
    return utils.is_bulb_coordinator_or_deputy(user)

@register.filter
def can_edit_book(user, book):
    return utils.can_edit_book(user, book)

@register.filter
def can_order_book(user, book):
    return utils.can_order_book(user, book)
