import functools

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404

from core.models import StudentClubYear
from clubs.models import Club
import clubs.utils

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
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='Media Center').exists()

def is_media_member(user):
    user_clubs = user.memberships.current_year()
    return user_clubs.filter(english_name='Media Center').exists()

def is_media_coordinator_or_member(user):
    user_clubs = clubs.utils.get_user_clubs(user)
    return user_clubs.filter(english_name='Media Center').exists()

def is_media_representative_of_club(user, club):
    return user in club.media_representatives.all()

def media_coordinator_or_member_test(user):
    if not is_media_coordinator_or_member(user) and not user.is_superuser:
        raise PermissionDenied
    else:
        return True

def media_user_test(user):
    if not is_media_coordinator_or_member(user) and \
       not user.is_superuser and \
       not user.media_representations.current_year().exists():
        raise PermissionDenied
    else:
        return True    
    
def is_club_coordinator_or_member(user):
    if not ((clubs.utils.is_coordinator_of_any_club(user) or clubs.utils.is_member_of_any_club(user)
             and not is_media_coordinator_or_member(user)) or user.is_superuser):
        raise PermissionDenied
    return True

def is_media_or_club_coordinator_or_member(user):
    if not (clubs.utils.is_coordinator_of_any_club(user) or clubs.utils.is_member_of_any_club(user) or user.is_superuser):
        raise PermissionDenied
    return True

def get_user_media_center(user):
    user_media_centers = clubs.utils.get_user_clubs(user).filter(english_name='Media Center')
    if user_media_centers.exists():
        return user_media_centers.first()
    else:
        return None

def can_assess_club_as_media_member(user, club):
    user_media_centers = clubs.utils.get_user_clubs(user).filter(english_name='Media Center',
                                                     city=club.city)

    return user_media_centers.exists()

def can_assess_club_as_media_coordinator(user, club):
    user_media_centers = clubs.utils.get_user_coordination_and_deputyships(user).filter(english_name='Media Center',
                                                                            city=club.city)

    return user_media_centers.exists()


def can_assess_club_as_media(user, club):
    user_media_centers = clubs.utils.get_user_clubs(user).filter(english_name='Media Center',
                                                     city=club.city)

    return user_media_centers.exists()

def can_submit_employeereport(user):
    return clubs.utils.is_employee_of_any_club(user) or \
        is_media_coordinator_or_member(user) or \
        clubs.utils.is_presidency_coordinator_or_deputy(user) or \
        user.has_perms('media.add_followupreport') or \
        user.is_superuser

def can_submit_studentreport(user, activity):
    return clubs.utils.has_coordination_to_activity(user, activity) or \
           is_media_coordinator_or_member(user) or \
           is_media_representative_of_club(user, activity.primary_club) or\
           clubs.utils.is_presidency_coordinator_or_deputy(user) or \
           user.has_perms('media.add_followupreport') or \
           user.is_superuser

def can_view_followupreport(user, activity):
    return can_submit_studentreport(user, activity) or \
        clubs.utils.is_member(activity.primary_club, user) or \
        clubs.utils.is_employee_of_any_club(user) or \
        clubs.utils.is_deanship_of_students_affairs_coordinator_or_member(user) or \
        user.has_perms('media.view_all_followupreports')

def get_clubs_for_assessment_by_user(user):
    user_assessing_clubs = clubs.utils.get_user_clubs(user).filter(can_assess=True)
    current_year_clubs = Club.objects.current_year().visible()
    # Filter the targetted clubs based on city and gender.
    if user_assessing_clubs.exists(): # Media or Presidency
        user_assessing_club = user_assessing_clubs.first()
        clubs_for_user = current_year_clubs.filter(city=user_assessing_club.city)
        # For MC members (and not coordinators or deputies), filter
        # the clubs based on the assigned clubs.
        if is_media_member(user) and not is_media_coordinator_or_deputy(user):
            # If the Media Center member is linked to specific clubs,
            # only show them the ones that they are linked to.  If
            # not, only show them the clubs that don't have anyone
            # linked to them.
            user_media_assessments = user.media_assessments.current_year()
            if user_media_assessments.exists():
                clubs_for_user = user_media_assessments
            else:
                clubs_for_user = clubs_for_user.filter(media_assessor__isnull=True)
    else: # Superuser
        clubs_for_user = current_year_clubs

    return clubs_for_user


def get_club_media_center(club):
    media_cetnrs = Club.objects.current_year().filter(english_name__contains="Media Center")
    if club.city == 'R':
        if club.gender:
            return media_cetnrs.get(city=club.city,
                                    gender=club.gender)
        else:
            return media_cetnrs.get(city=club.city,
                                    gender='M')
    else:
        return media_cetnrs.get(city=club.city)
