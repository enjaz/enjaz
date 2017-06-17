import datetime
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from bulb.models import Request
from django.utils import timezone
from post_office import mail
from media.utils import get_club_media_center


class Command(BaseCommand):
    help = "Notify users on pending requests after 3 days."

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        date = timezone.now().date() - datetime.timedelta(3)
        date_min = datetime.datetime.combine(date, datetime.time.min)
        date_max = datetime.datetime.combine(date, datetime.time.max)
        for book_request in Request.objects.filter(delivery='D')\
                                           .filter(submission_date__range=(date_min, date_max))\
                                           .filter(requester_status='', owner_status=''):
            full_url = "https://{}{}#{}".format(domain,
                                                reverse('bulb:requests_to_me'),
                                                book_request.pk)
            email_context = {'book_request': book_request,
                             'full_url': full_url}
            mail.send([book_request.book.submitter.email],
                       template="pending_book_request_to_owner",
                       context=email_context)
            mail.send([book_request.requester.email],
                       template="pending_book_request_to_requester",
                       context=email_context)
            self.stdout.write(u'Emailed {} and {} on {}.'.format(book_request.book.submitter.username,
                                                                 book_request.requester.username,
                                                                 book_request.book.title))
