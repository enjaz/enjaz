from django.template import Library
from arshidni import utilities
register = Library()

@register.filter
def has_current_colleague_profile(user):
    return user.colleague_profiles.current_year().exists()

@register.filter
def is_arshindi_coordinator_or_deputy(user):
    return utilities.is_arshindi_coordinator_or_deputy(user)
