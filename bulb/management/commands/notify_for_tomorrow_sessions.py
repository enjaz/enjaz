import datetime
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from bulb.models import Session
from django.utils import timezone
from post_office import mail
from media.utils import get_club_media_center


class Command(BaseCommand):
    help = "Notify users on session occurring tomorrow."

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        date = timezone.now().date() + datetime.timedelta(1)
        for session in Session.objects.filter(date=date, is_deleted=False):
            full_url = "https://{}{}#{}".format(domain,
                                                reverse('bulb:show_group'),
                                                session.group.pk)
            email_context = {'session': session}
            for membership in session.group.membership_set.filter(is_active=True):
                email_context['user'] = membership.user
                mail.send([membership.user.email],
                           template="tomorrow_session_reminder_to_member",
                           context=email_context)
                self.stdout.write(u'Emailed {} and {} on {}.'.format(membership.user.username,
                                                                     session.title))
