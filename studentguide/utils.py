from accounts.utils import get_user_gender
from studentguide.models import GuideProfile
from clubs.models import Club
import clubs.utils

def is_studentguide_member(user):
    user_clubs = user.memberships.current_year()
    return user_clubs.filter(english_name='Student Guide').exists()

def is_studentguide_coordinator_or_deputy(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='Student Guide').exists()

def get_studentguide_club_of_user(user):
    user_clubs = clubs.utils.get_user_clubs(user)
    studentguide = user_clubs.filter(english_name='Student Guide')
    if studentguide.exists():
        return studentguide.first()
    else:
        return None

def get_studentguide_club_for_user(user):
    user_gender = get_user_gender(user)
    if user_gender == 'F':
        return Club.objects.current_year().get(english_name="Student Guide",
                                               gender="F")
    else:
        return Club.objects.current_year().get(english_name="Student Guide",
                                               gender="M")

    
def has_guide_profile(user):
    return GuideProfile.objects.current_year().filter(user=user).exists()

def get_user_guide_profile(user):
    return GuideProfile.objects.current_year().filter(user=user).first()

def can_edit_guide(user, guide):
    if is_studentguide_coordinator_or_deputy(user) or \
       user.is_superuser or \
       guide.user == user:
        return True
    else:
        return False

def can_add_request(user, guide):
    # If the guide has reached the maxmium student number, don't allow
    # new request submission.  For testing purposes, coordinators and
    # superusers can always add requests.  Otherwise, if the user has
    # a GuideProfile, they are not expected to submit a supervision
    # request.
    if get_user_gender(user) != get_user_gender(guide.user) or \
       guide.guide_requests.filter(user=user).exclude(requester_status='C',
                                                      guide_status='P').exists() or \
       not guide.is_available:
        return False
    elif is_studentguide_coordinator_or_deputy(user) or \
         user.is_superuser or \
         not has_guide_profile(user):
        return True
    else:
        return False

def can_edit_request(user, guide_request):
    if is_studentguide_coordinator_or_deputy(user) or \
       user.is_superuser or \
       guide_request.user == user:
        return True
    else:
        return False

def is_guide_of_user(guide, user):
    return guide.guide_requests.filter(user=user, guide_status='A',
                                       requester_status='A').exists()

def has_pending_request(user, guide):
    return guide.guide_requests.pending().filter(user=user).exists()
