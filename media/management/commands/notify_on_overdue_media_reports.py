from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.utils import timezone, translation

from activities.models import Episode
from post_office import mail


class Command(BaseCommand):
    help = 'This script runs once every Sunday to notify media representatives and clubs employees about episodes with missing reports for any episode that ended on any previous day (excluding Sunday itself, because another notification would have already been sent).'

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        domain = Site.objects.get_current().domain
        end_date_target = timezone.now().date()
        for episode in Episode.objects.filter(activity__is_approved=True,
                                              requires_report=True,
                                              end_date__lt=end_date_target)\
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
                print episode.activity.primary_club.employee.email
                mail.send([episode.activity.primary_club.employee.email],
                          template="overdue_report_to_report_submitter",
                          context=email_context)
            if not episode.report_is_submitted():
                emails = episode.activity.primary_club.media_representatives.values_list('email', flat=True)
                if emails:
                    full_url = "https://{}{}".format(domain,
                                                     reverse('media:submit_report',
                                                             args=(episode.pk,)))
                    email_context['full_url'] = full_url
                    mail.send(list(emails),
                              template="overdue_report_to_report_submitter",
                              context=email_context)
