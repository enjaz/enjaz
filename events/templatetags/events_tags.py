from django import template

from events import utils


register = template.Library()

@register.filter
def is_organizing_committee_member(user, event):
    return utils.is_organizing_committee_member(user, event)

@register.filter
def has_user_organizing_events(user):
    return utils.get_user_organizing_events(user).exists()

@register.filter
def get_user_organizing_events(user):
    return utils.get_user_organizing_events(user)

@register.filter
def get_session_priority(registration, session):
    if session in registration.first_priority_sessions.all():
        return 1
    elif session in registration.second_priority_sessions.all():
        return 2
