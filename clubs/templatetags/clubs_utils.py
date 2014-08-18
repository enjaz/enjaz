from django import template
from clubs.utils import *

register = template.Library()

@register.simple_tag
def is_coordinator_of_any_club(user):
    return is_coordinator_of_any_club(user)

@register.simple_tag
def is_member_of_any_club(user):
    return is_member_of_any_club(user)

@register.simple_tag
def is_coordinator(club, user):
    return is_coordinator(club, user)

@register.simple_tag
def is_member(club, user):
    return is_member(club, user)

@register.simple_tag
def is_coordinator_or_member(club, user):
    return is_coordinator_or_member(club, user)

@register.simple_tag
def get_presidency():
    return get_presidency()

@register.simple_tag
def get_media_center():
    return get_media_center()