import functools

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404

from core.models import StudentClubYear
from clubs.models import Club
from clubs.utils import is_coordinator_or_member, is_coordinator_of_any_club, is_member_of_any_club, is_coordinator_or_member, get_media_center, get_user_clubs, get_user_coordination_and_deputyships,  has_coordination_to_activity


current_year = StudentClubYear.objects.get_current()

WHAT_IF_URL = "whatif"
HUNDRED_SAYS_URL = "100says"
WHAT_IF = 0
HUNDRED_SAYS = 1


# Constants
REPORT_DUE_AFTER = 7  # in days
MAX_OVERDUE_REPORTS = 3

def proper_poll_type(view_func):
    """
    A wrapper to ensure the passed ``poll_type`` is valid, then convert that from a url
    to a poll_type easily understood by the view.
    """
    @functools.wraps(view_func)
    def wrapper(request, poll_type, *args, **kwargs):
        if poll_type == WHAT_IF_URL:
            simple_poll_type = WHAT_IF
        elif poll_type == HUNDRED_SAYS_URL:
            simple_poll_type = HUNDRED_SAYS
        else:
            raise Http404
        return view_func(request, poll_type=simple_poll_type, *args, **kwargs)
    return wrapper

def get_poll_type_url(poll_type):
    """
    Return the appropriate url keyword for the passed poll type.
    """
    if poll_type == WHAT_IF:
        return WHAT_IF_URL
    elif poll_type == HUNDRED_SAYS:
        return HUNDRED_SAYS_URL

def is_media_coordinator_or_deputy(user):
    coordination_and_deputyships = get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='Media Center').exists()

def is_media_member(user):
    user_clubs = user.memberships.current_year()
    return user_clubs.filter(english_name='Media Center').exists()

def is_media_coordinator_or_member(user):
    user_clubs = get_user_clubs(user)
    return user_clubs.filter(english_name='Media Center').exists()

def media_coordinator_or_member_test(user):
    if not is_media_coordinator_or_member(user) and not user.is_superuser:
        raise PermissionDenied
    else:
        return True

def is_club_coordinator_or_member(user):
    if not ((is_coordinator_of_any_club(user) or is_member_of_any_club(user)
             and not is_media_coordinator_or_member(user)) or user.is_superuser):
        raise PermissionDenied
    return True

def is_media_or_club_coordinator_or_member(user):
    if not (is_coordinator_of_any_club(user) or is_member_of_any_club(user) or user.is_superuser):
        raise PermissionDenied
    return True

def get_user_media_center(user):
    user_media_centers = get_user_clubs(user).filter(english_name='Media Center')
    if user_media_centers.exists():
        return user_media_centers.first()
    else:
        return None

def can_assess_club_as_media_member(user, club):
    user_media_centers = get_user_clubs(user).filter(english_name='Media Center',
                                                     city=club.city)

    if club.city == 'R':
        user_media_centers = user_media_centers.filter(gender=club.gender)

    return user_media_centers.exists()

def can_assess_club_as_media_coordinator(user, club):
    user_media_centers = get_user_coordination_and_deputyships(user).filter(english_name='Media Center',
                                                                            city=club.city)

    if club.city == 'R':
        user_media_centers = user_media_centers.filter(gender=club.gender)

    return user_media_centers.exists()


def can_assess_club_as_media(user, club):
    user_media_centers = get_user_clubs(user).filter(english_name='Media Center',
                                                     city=club.city)

    if club.city == 'R':
        user_media_centers = user_media_centers.filter(gender=club.gender)

    return user_media_centers.exists()

def can_submit_followupreport(user, activity):
    return has_coordination_to_activity(user, activity) or \
           user in activity.primary_club.media_representatives.all() or \
           is_media_coordinator_or_member(user) or \
           user.is_superuser

def get_clubs_for_assessment_by_user(user):
    user_assessing_clubs = get_user_clubs(user).filter(can_assess=True)
    current_year_clubs = Club.objects.current_year().visible()
    # Filter the targetted clubs based on city and gender.
    if user_assessing_clubs.exists(): # Media or Presidency
        user_assessing_club = user_assessing_clubs.first()
        clubs_for_user = current_year_clubs.filter(city=user_assessing_club.city)
        if user_assessing_club.city == 'R':
            clubs_for_user = clubs_for_user.filter(gender=user_assessing_club.gender)
    else: # Superuser
        clubs_for_user = current_year_clubs

    return clubs_for_user
