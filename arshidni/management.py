from django.contrib.auth.models import Permission, User, Group
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_syncdb

import arshidni.models

def create_groups(sender, **kwargs):
    # In order for the coordinator to be able to use the Arshindi
    # Admin interface, we create a group for them.
    try:
        arshidni_group = Group.objects.get(name='arshidni')
    except ObjectDoesNotExist:
        arshidni_group = Group.objects.create(name='arshidni')

    change_studygroup = Permission.objects.get(codename='change_studygroup')
    change_question = Permission.objects.get(codename='change_question')
    change_answer = Permission.objects.get(codename='change_answer')
    change_graduateprofile = Permission.objects.get(codename='change_graduateprofile')
    change_learningobjective = Permission.objects.get(codename='change_learningobjective')
    change_joinstudygrouprequest = Permission.objects.get(codename='change_joinstudygrouprequest')
    change_colleagueprofile = Permission.objects.get(codename='change_colleagueprofile')
    change_supervisionrequest = Permission.objects.get(codename='change_supervisionrequest')
    delete_studygroup = Permission.objects.get(codename='delete_studygroup')
    delete_question = Permission.objects.get(codename='delete_question')
    delete_answer = Permission.objects.get(codename='delete_answer')
    delete_graduateprofile = Permission.objects.get(codename='delete_graduateprofile')
    delete_learningobjective = Permission.objects.get(codename='delete_learningobjective')
    delete_joinstudygrouprequest = Permission.objects.get(codename='delete_joinstudygrouprequest')
    delete_colleagueprofile = Permission.objects.get(codename='delete_colleagueprofile')
    delete_supervisionrequest = Permission.objects.get(codename='delete_supervisionrequest')

    arshidni_group.permissions.add(change_studygroup, change_question,
                                   change_answer,
                                   change_graduateprofile,
                                   change_learningobjective,
                                   change_joinstudygrouprequest,
                                   change_colleagueprofile,
                                   change_supervisionrequest,
                                   delete_studygroup, delete_question,
                                   delete_answer,
                                   delete_graduateprofile,
                                   delete_learningobjective,
                                   delete_joinstudygrouprequest,
                                   delete_colleagueprofile,
                                   delete_supervisionrequest)
    arshidni_group.save()

post_syncdb.connect(create_groups, sender=arshidni.models)
