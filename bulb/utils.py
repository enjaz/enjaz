from clubs.models import Club
import clubs.utils
from accounts.utils import get_user_gender
from bulb.models import MAXIMUM_GROUP_MEMBERS

def is_bulb_coordinator_or_deputy(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='Bulb').exists()

def is_bulb_member(user):
    user_clubs = user.memberships.current_year()
    return user_clubs.filter(english_name='Bulb').exists()

def get_bulb_club_for_user(user):
    user_gender = get_user_gender(user)
    if user_gender == 'F':
        return Club.objects.current_year().get(english_name="Bulb",
                                               gender="F")
    else:
        return Club.objects.current_year().get(english_name="Bulb",
                                               gender="M")

def get_indirect_request_cc(book):
    """Bulb members are those who are assigned indirect requests."""
    bulb_club = get_bulb_club_for_user(book.submitter)
    return [member.email for member in bulb_club.members.all()]

def get_session_submitted_cc(group):
    bulb_club = get_bulb_club_for_user(group.coordinator)
    return [deputy.email for deputy in bulb_club.deputies.all()]

def get_bulb_club_of_user(user):
    user_clubs = clubs.utils.get_user_clubs(user)
    bulb = user_clubs.filter(english_name='Bulb')
    if bulb.exists():
        return bulb.first()
    else:
        return None

def can_edit_book(user, book):
    # If the book is unavailable the owner cannot edit it.
    if not book.is_available and \
       book.submitter == user:
        return False
    elif is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       book.submitter == user:
        return True
    else:
        return False

def can_edit_owner_status(user, book):
    if is_bulb_coordinator_or_deputy(user) or \
       is_bulb_member(user) or \
       user.is_superuser or \
       book.submitter == user:
        return True
    else:
        return False

def can_edit_requester_status(user, book_request):
    if is_bulb_coordinator_or_deputy(user) or \
       is_bulb_member(user) or \
       user.is_superuser or \
       user == book_request.requester:
        return True
    else:
        return False
    
def can_order_book(user, book):
    if book.is_deleted or \
       user == book.submitter or \
       not book.is_available:
        return False
    else:
        return True

def can_edit_group(user, group):
    if is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       group.coordinator == user:
        return True
    else:
        return False

def group_can_have_sessions(group):
    return True
    if not group.is_deleted and \
       group.membership_set.filter(is_active=True).count() >= 3:
        return True
    else:
        return False

def can_join_group(user, group):
    if group.is_deleted or \
       group.membership_set.filter(user=user).exists() or \
       group.membership_set.active().count() > MAXIMUM_GROUP_MEMBERS or \
       group.coordinator == user or \
       (group.gender and get_user_gender(user) != group.gender) or \
       group.membership_set.filter(user=user).exists():
        return False
    else:
        return True

   #get_user_gender(group.coordinator) != group.coordinator(user) or \

def is_active_group_member(user, group):
    return group.membership_set.filter(user=user, is_active=True).exists()
    
def can_edit_reader_profile(user, reader_profile):
    if is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       reader_profile.user == user:
        return True
    else:
        return False
