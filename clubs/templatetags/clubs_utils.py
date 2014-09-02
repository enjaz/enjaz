from django import template
from clubs import utils

register = template.Library()

@register.filter
def is_coordinator_of_any_club(user):
    return utils.is_coordinator_of_any_club(user)

@register.filter
def is_member_of_any_club(user):
    return utils.is_member_of_any_club(user)

@register.filter
def is_coordinator(user, club):
    return utils.is_coordinator(club, user)

@register.filter
def is_member(user, club):
    return utils.is_member(club, user)

@register.filter
def is_coordinator_or_member(user, club):
    return utils.is_coordinator_or_member(club, user)
#
# @register.filter
# def get_presidency():
#     return utils.get_presidency()
#
# @register.filter
# def get_media_center():
#     return utils.get_media_center()