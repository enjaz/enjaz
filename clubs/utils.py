"""Utility functions related to the clubs app."""
from .models import Club
from core.models import StudentClubYear

def is_coordinator_of_any_club(user):
    """Return whether the user is a coordinator of any club."""
    return user.coordination.current_year().filter(can_submit_activities=True).exists()

def is_deputy_of_any_club(user):
    """Return whether the user is a deputy of any club."""
    return Club.objects.current_year().filter(deputies=user).exists()

def is_member_of_any_club(user):
    """Return whether the user is a member of any club."""
    return user.memberships.current_year().exists()

def is_employee_of_any_club(user):
    """Return whether the user is an employee of any club."""
    employee_clubs = Club.objects.current_year().filter(employee=user)
    return employee_clubs.exists()

def is_coordinator(club, user):
    """Return whether the user is the coordinator of a given club."""
    return club.coordinator == user

def is_deputy(club, user):
    """Return whether the user is a member of a given club."""
    if not user.is_authenticated():
        return False
    return user in club.deputies.filter(pk=user.pk)

def is_member(club, user):
    """Return whether the user is a member of a given club."""
    if not user.is_authenticated():
        return False
    return user in club.members.filter(pk=user.pk)

def is_coordinator_or_member(club, user):
    """Return whether the user is the coordinator, a deputy or a member of a given club."""
    return is_coordinator(club, user) or is_deputy(club, user) or is_member(club, user)

def is_coordinator_or_deputy(club, user):
    """Return whether the user is the coordinator or a deputy of a given club."""
    return is_coordinator(club, user) or is_deputy(club, user)

def is_employee(club, user):
    """Return whether the user is the employee assigned to a given club."""
    return user == club.employee

def has_coordination_to_activity(user, activity):
    """Return whether the user is the coordinator or deputy assigned to
    any of the primry or secondary clubs of a given activity.
    """
    if not user.is_authenticated():
        return False
    # First get clubs associated with the activity.  We need both of
    # them to be QuerySets
    activity_primary_club = Club.objects.filter(
                            id=activity.primary_club.id)
    activity_secondary_clubs = activity.secondary_clubs.all()
    activity_clubs = activity_primary_club | activity_secondary_clubs
    # Second, check if any of which have the given user as a
    # coordinator or deputy
    coordination_clubs = activity_clubs.filter(coordinator=user) | \
                         activity_clubs.filter(deputies=user)
    # Return a Boolean 
    return coordination_clubs.exists()

def get_deanship():
    return Club.objects.current_year().get(english_name="Deanship of Student Affairs")

def get_presidency():
    return Club.objects.current_year().get(english_name="Presidency")

def get_media_center():
    return Club.objects.current_year().get(english_name="Media Center",
                                           city='R', gender='M')

def get_user_clubs(user):
    if not user.is_authenticated():
        return Club.objects.none()
    return user.memberships.current_year() | user.deputyships.current_year() | user.coordination.current_year()

def get_user_coordination_and_deputyships(user):
    """Return the clubs in which the given user is the coordinator or
    deputy.  Returns None if no clubs are found."""
    if not user.is_authenticated():
        return Club.objects.none()

    coordination = user.coordination.current_year()
    deputyships = user.deputyships.current_year()
    # Return a QuerySet to allow further filtering
    return (coordination | deputyships)

def is_presidency_coordinator_or_deputy(user):
    coordination_and_deputyships = get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name__contains='Presidency').exists()

def is_deanship_of_students_affairs_coordinator_or_member(user):
    """Return whether the user is an employee of any club."""
    return get_user_clubs(user).filter(english_name__contains='Deanship of Student Affairs').exists()

def is_coordinator_or_deputy_of_any_club(user):
    """Return whether the user is a coordinator of any club."""
    coordination_and_deputyships = get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.exists()

def forms_editor_check(user, object):
    """A function to evaluate if user is eligible to create/edit forms for clubs."""
    # Confirm that the passed object is a ``Club`` instance
    if not isinstance(object, Club):
        raise TypeError("Expected a Club object, received %s" % type(object))
    return is_coordinator_or_deputy(object, user) or user.is_superuser

def can_review_activity(user, activity):
    if not user.is_authenticated():
        return False
    elif user.has_perm('activities.add_review'): # e.g. superuser
        return True
    reviewing_parents = Club.objects.activity_reviewing_parents(activity)
    user_clubs = reviewing_parents.filter(coordinator=user) | \
                 reviewing_parents.filter(deputies=user)
    return user_clubs.exists()

def can_delete_activity(user, activity):
    # A user can delete an activity in three cases:
    # * If they have the change_activity permission (e.g. superuser).
    # * If they are the submitter, coordinator or deputy and the
    #   activity is not reviewed yet.
    # * If they are the coordinator or deputy of any club that can
    #   review the activity, if that club has can_delete=True.  In
    #   real life, this means vice presidents.
    if not user.is_authenticated():
        return False
    elif user.has_perm('activities.change_activity'):
        return True
    elif activity.is_editable and \
       not activity.review_set.exists() and \
       (activity.submitter == user or \
       has_coordination_to_activity(user, activity)):
        return True
    else:
        reviewing_parents = Club.objects.activity_reviewing_parents(activity)
        deleting_parents = reviewing_parents.filter(can_delete=True)
        user_clubs = deleting_parents.filter(coordinator=user) | deleting_parents.filter(deputies=user)
        return user_clubs.exists()

def can_edit_activity(user, activity):
    # A user can edit an activity in three cases:
    # * If they have the change_activity permission (e.g. superuser).
    # * If they are the submitter, coordinator or deputy and the
    #   activity is_editable=True.
    # * If they are the coordinator or deputy of any club that can
    #   review the activity, if that club has can_edit=True.  In
    #   real life, this means vice presidents.
    if not user.is_authenticated():
        return False
    elif user.has_perm('activities.change_activity'):
        return True
    elif activity.is_approved == False and \
         (activity.submitter == user or \
         has_coordination_to_activity(user, activity)):
        return False
    elif (activity.submitter == user or \
          has_coordination_to_activity(user, activity)):
        # This doesn't necessarily mean that they would be able to
        # edit the activity fully.  Further restriction is to be
        # imposed in the view.
        return True
    else:
        reviewing_parents = Club.objects.activity_reviewing_parents(activity)
        editing_parents = reviewing_parents.filter(can_edit=True)
        user_clubs = editing_parents.filter(coordinator=user) | editing_parents.filter(deputies=user)
        return user_clubs.exists()

def can_review_any_niqati(user):
    if not user.is_authenticated():
        return False
    elif user.has_perm('activities.change_activity'): # e.g. superuser
        return True
    niqati_reviewers = Club.objects.filter(can_review_niqati=True)
    user_clubs = niqati_reviewers.filter(coordinator=user) | \
                 niqati_reviewers.filter(deputies=user)
    return user_clubs.exists()

def get_order_reviewing_clubs_by_user(user, order):
    if not user.is_authenticated():
        return Club.objects.none()
    niqati_reviewers = Club.objects.niqati_reviewing_parents(order)
    user_clubs = niqati_reviewers.filter(coordinator=user) | \
                 niqati_reviewers.filter(deputies=user)
    return user_clubs


def can_submit_activities(user):
    if not user.is_authenticated():
        return False
    elif user.has_perm('activities.add_activity'): # e.g. superuser
        return True
    else:
        coordination_and_deputyships = get_user_coordination_and_deputyships(user)
        return coordination_and_deputyships.filter(can_submit_activities=True).exists()
