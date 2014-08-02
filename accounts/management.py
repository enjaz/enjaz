from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_syncdb
import accounts.models

def create_groups(sender, **kwargs):
    # In order for the employees to be able to use the Deanship Admin
    # interface, we create a group for them.  Further more, we make
    # them able to see the deanship review.
    deanship_group = Group.objects.create(name='deanship')
    view_deanship_review = Permission.objects.get(codename='view_deanship_review')
    deanship_group.permissions.add(view_deanship_review)
    deanship_group.save()

    # This group is meant for the President of the Studnet Club and
    # his deputies.
    presidency_group = Group.objects.create(name='presidency')
    add_activity = Permission.objects.get(codename='add_activity')
    directly_add_activity = Permission.objects.get(codename='directly_add_activity')
    # The 'change_activity' permission indicates that the user can
    # changes activities regardless of the value of is_editable.
    change_activity = Permission.objects.get(codename='change_activity')
    # The 'view_activity' permission indicates that thie user can view
    # activities regardless of whether or not they have been approved.
    view_activity = Permission.objects.get(codename='view_activity')
    view_participation = Permission.objects.get(codename='view_participation')
    add_club = Permission.objects.get(codename='add_club')
    change_club = Permission.objects.get(codename='change_club')
    # change_book = Permission.objects.get(codename='change_book')
    # delete_book = Permission.objects.get(codename='delete_book')
    view_presidency_review = Permission.objects.get(codename='view_presidency_review')
    add_presidency_review = Permission.objects.get(codename='add_presidency_review')
    presidency_group.permissions.add(add_activity,
                                     directly_add_activity,
                                     change_activity, view_activity,
                                     view_participation, add_club,
                                     change_club, #change_book,
                                     view_presidency_review,
                                     view_deanship_review,
                                     add_presidency_review)
    presidency_group.save()
post_syncdb.connect(create_groups, sender=accounts.models)
