from clubs.models import Club
from clubs.utils import get_user_coordination_and_deputyships
from accounts.utils import get_user_gender

def is_bulb_coordinator_or_deputy(user):
    coordination_and_deputyships = get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='Bulb').exists()

def get_bulb_club_for_user(user):
    user_gender = get_user_gender(user)
    if user_gender == 'F':
        return Club.objects.current_year().get(english_name="Bulb",
                                               gender="F")
    else:
        return Club.objects.current_year().get(english_name="Bulb",
                                               gender="M")

def get_bulb_club_of_user(user):
    coordination_and_deputyships = get_user_coordination_and_deputyships(user)
    bulb = coordination_and_deputyships.filter(english_name='Bulb')
    if bulb.exists():
        return bulb.first()
    else:
        return None

def can_edit_book(user, book):
    if is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       book.submitter == user:
        return True
    else:
        return False

def can_order_book(user, book):
    if user == book.submitter or \
       not book.is_available or \
       book.is_deleted:
        return False
    else:
        return True
