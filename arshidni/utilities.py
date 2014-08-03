from django.contrib.auth.models import Group

def get_arshidni_coordinator():
    arshidni_group = Group.objects.get(name='arshidni')
    return arshidni_group.members.all()[0]
