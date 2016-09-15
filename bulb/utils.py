# -*- coding: utf-8  -*-
import datetime
from django.utils import timezone
from django.db import IntegrityError

from clubs.models import Club
from core.models import Tweet
import accounts.utils
import clubs.utils


def create_tweet(user, action, arguments):
    if not user.social_auth.exists():
        return
    if action == "add_book":
	text = u"أضفت كتاب {} إلى المكتبة الطلابية التعاونية!\nيمكن طلبه الآن: {}\n#مبادرة_سِراج"
    if action == "add_needed_book":
	text = u"أريد كتاب {}.\nهل يتوفّر لديك؟: {}\n#مبادرة_سِراج"
    elif action == "join_group":
	text = u"انضممت إلى مجموعة {} للنقاش والقراءة!\nيمكن الانضمام الآن: {}\n#مبادرة_سِراج"
    elif action == "add_group":
	text = u"أنشأت مجموعة {} للنقاش والقراءة!\nيمكن الانضمام الآن: {}\n#مبادرة_سِراج"
    elif action == "add_reader":
	text = u"سجّلت نفسي مع قارئات وقراء الجامعة.  يمكن أن تقرأ صفحتي من هنا:  {}\n#مبادرة_سِراج"
    elif action == "add_session":
	text = u"أعلنت عن جلسة نقاش عن {} يمكنك تسجيل نفسك ضمن الحضور هنا: {}\n#مبادرة_سِراج"

    try:
        Tweet.objects.create(text=text.format(*arguments), user=user)
    except IntegrityError:
        # If the tweet turned to be longer than 140 charecters, just don't do anything.
        pass

def is_bulb_coordinator_or_deputy(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='Bulb').exists()

def is_bulb_member(user):
    if not user.is_authenticated():
        return False
    user_clubs = user.memberships.current_year()
    return user_clubs.filter(english_name='Bulb').exists()

def get_bulb_club_for_user(user):
    return clubs.utils.get_club_for_user("Bulb", user)

def get_indirect_request_cc(book):
    """Bulb members are those who are assigned indirect requests."""
    bulb_club = get_bulb_club_for_user(book.submitter)
    return [member.email for member in bulb_club.members.all()]

def get_session_submitted_cc(session):
    bulb_club = get_bulb_club_for_user(session.submitter)
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

def can_edit_needed_book(user, needed_book):
    if is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       needed_book.requester == user:
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

def can_edit_session(user, session):
    if session.group and user == session.group.coordinator or \
       is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       session.submitter == user:
        return True
    else:
        return False

def group_can_have_sessions(group):
    if not group.is_deleted and \
       not group.is_archived and \
       group.membership_set.filter(is_active=True).count() >= 3:
        return True
    else:
        return False

def can_attend_session(user, session):
    session_datetime = timezone.make_aware(datetime.datetime.combine(session.date, session.start_time), timezone.get_default_timezone())
    if session.is_deleted or \
       timezone.now() > session_datetime or \
       session.confirmed_attendees.filter(pk=user.pk).exists() or \
       session.submitter == user or \
       (session.is_limited_by_gender and accounts.utils.get_user_gender(user) != accounts.utils.get_user_gender(session.submitter)) or \
       (session.is_limited_by_city and accounts.utils.get_user_city(user) != accounts.utils.get_user_city(session.submitter)):
        return False
    else:
        return True

def can_join_group(user, group):
    if group.is_deleted or \
       group.membership_set.filter(user=user).exists() or \
       group.coordinator == user or \
       (group.is_limited_by_gender and accounts.utils.get_user_gender(user) != accounts.utils.get_user_gender(group.coordinator)) or \
       (group.is_limited_by_city and accounts.utils.get_user_city(user) != accounts.utils.get_user_city(group.coordinator)):
        return False
    else:
        return True

def is_active_group_member(user, group):
    return group.membership_set.filter(user=user, is_active=True).exists()
    
def can_edit_reader_profile(user, reader_profile):
    if is_bulb_coordinator_or_deputy(user) or \
       user.is_superuser or \
       reader_profile.user == user:
        return True
    else:
        return False
