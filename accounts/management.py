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
    presidency_gruop = Group.objects.create(name='presidency')
    view_presidency_review = Permission.objects.get(codename='view_presidency_review')
    add_presidency_review = Permission.objects.get(codename='add_presidency_review')
    directly_add_activity = Permission.objects.get(codename='directly_add_activity')
    presidency_gruop.permissions.add(view_presidency_review,
                                     add_presidency_review,
                                     directly_add_activity)

post_syncdb.connect(create_groups, sender=accounts.models)
