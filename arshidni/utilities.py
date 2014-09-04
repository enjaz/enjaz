from django.contrib.auth.models import Group

def get_arshidni_coordinator():
    arshidni_group = Group.objects.get(name='arshidni')
    return arshidni_group.user_set.all()[0]
