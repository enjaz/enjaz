from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation, timezone
from django.contrib.auth.models import User

from post_office import mail

class Command(BaseCommand):
    help = "Send reminding emails."

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        tomorrow_date = timezone.now().date() + timezone.timedelta(days=1)

        for invitation in Invitation.objects.filter(date=tomorrow_date, is_deleted=False):
            tomorrow_registrations = invitation.students.filter(date=tomorrow_date,
                                                                       is_deleted=False)
            invitation = tomorrow_registrations.first().invitation


            email_context = {'invitation': invitation,
                             'tomorrow_date': tomorrow_date,
                             'tomorrow_registrations':
                             tomorrow_registrations}
            mail.send([user.email],
                       template="invitation_reminder",
context=email_context)
