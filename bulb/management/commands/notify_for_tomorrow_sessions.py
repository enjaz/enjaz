import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils import translation

from bulb.models import Session
from django.utils import timezone
from post_office import mail
from bulb import utils


class Command(BaseCommand):
    help = "Notify users on session occurring tomorrow."

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        domain = Site.objects.get_current().domain
        date = timezone.now().date() + datetime.timedelta(1)
        for session in Session.objects.filter(date=date, is_deleted=False):
            full_url = "https://{}{}#session-{}".format(domain,
                                                        reverse('bulb:show_group', args=(session.group.pk,)),
                                                        session.pk)
            email_context = {'session': session, 'full_url': full_url}
            for membership in session.group.membership_set.filter(is_active=True):
                email_context['member'] = membership.user
                mail.send([membership.user.email],
                           template="reading_group_session_reminder",
                           context=email_context)
                self.stdout.write(u'Emailed {} on {}.'.format(membership.user.username,
                                                                     session.title))

            # Also send it to the group coordinator
            email_context['member'] = session.group.coordinator
            mail.send([session.group.coordinator.email],
                       template="reading_group_session_reminder",
                       context=email_context)

            # Also, send it to the Bulb coordinator.
            bulb_coordinator = utils.get_bulb_club_for_user(session.group.coordinator).coordinator
            email_context['member'] = bulb_coordinator
            cc = utils.get_session_submitted_cc(session.group)
            mail.send([bulb_coordinator.email],
                      cc=cc,
                      template="reading_group_session_reminder",
                      context=email_context)
