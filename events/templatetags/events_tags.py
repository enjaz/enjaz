from django import template

from events import utils
from events.models import SessionRegistration

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

@register.filter
def is_registered(user, session):
    return utils.is_registered(user, session)

@register.filter
def get_status(user, session):
    session_registration = SessionRegistration.objects.get(session=session, user=user)
    if session_registration.is_deleted:
        return False
    else:
        return session_registration.is_approved

@register.filter
def is_on_sidebar(user, event):
    return event.is_on_sidebar(user)
