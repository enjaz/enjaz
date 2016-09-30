from datetime import timedelta

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils import timezone, translation

from activities.models import Episode
from post_office import mail


class Command(BaseCommand):
    help = 'This script runs every ten minutes to notify media representaives and club employees that an episode has a required report right after it is done.'

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        domain = Site.objects.get_current().domain
        end_date_target = timezone.now().date()
        end_time_since = (timezone.now() - timedelta(minutes=10)).time()
        end_time_until = timezone.now().time()
        for episode in Episode.objects.filter(activity__is_approved=True,
                                              requires_report=True,
                                              end_date=end_date_target,
                                              end_time__gt=end_time_since,
                                              end_time__lte=end_time_until)\
                                      .exclude(followupreport__isnull=False,
                                               employeereport__isnull=False):
            print episode
            email_context = {'episode': episode}

            if not episode.employee_report_is_submitted() and \
               episode.activity.primary_club.employee:
                full_url = "https://{}{}".format(domain,
                                                 reverse('media:submit_employee_report',
                                                         args=(episode.pk,)))
                email_context['full_url'] = full_url
                mail.send([episode.activity.primary_club.employee.email],
                          template="due_report_to_report_submitter",
                          context=email_context)
            if not episode.report_is_submitted():
                emails = episode.activity.primary_club.media_representatives.values_list('email', flat=True)
                if emails:
                    full_url = "https://{}{}".format(domain,
                                                     reverse('media:submit_report',
                                                             args=(episode.pk,)))
                    email_context['full_url'] = full_url
                    mail.send(list(emails),
                              template="due_report_to_report_submitter",
                              context=email_context)
