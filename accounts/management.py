from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_syncdb
import accounts.models

def create_permissions(sender, **kwargs):
    user_type = ContentType.objects.get_for_model(User)
    Permission.objects.create(content_type=user_type,
                              codename='deanship_employee',
                              name="Deanship employee")

post_syncdb.connect(create_permissions, sender=accounts.models)
