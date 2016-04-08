import datetime
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from bulb.models import Request, Report
from core.models import StudentClubYear
from niqati.models import Code
import niqati.utils


class Command(BaseCommand):
    help = "Create codes for previous Bulb events."

    def handle(self, *args, **options):
        current_year = StudentClubYear.objects.get_current()
        # For book requests, we want to create niqati codes for
        # requests that have neen confirmed by either:
        # 1) the owner,
        # 2) the requester,
        # 3) both the requester and the owner.
        # All requests must not have existing codes.
        request_content_type = ContentType.objects.get(app_label="bulb", model="request")
        previous_request_pks = Code.objects.filter(content_type=request_content_type)\
                                           .values_list('object_id', flat=True)
        included_requests = (Request.objects.filter(requester_status__in=["", "F"],
                                                    owner_status__in=["R", "D"]) | \
                             Request.objects.filter(requester_status__in=["R", "D"],
                                                    owner_status__in=["", "F"]) | \
                             Request.objects.filter(requester_status__in=["R", "D"],
                                                    owner_status__in=["R", "D"]))\
                                            .filter(delivery='D')\
                                            .exclude(pk__in=previous_request_pks)

        string_count = included_requests.count()
        random_strings = niqati.utils.get_free_random_strings(string_count)
        counter = 0

        for book_request in included_requests:
            book_request.create_related_niqati_codes(random_strings[counter])
            counter += 1
            self.stdout.write(u'Add niqati to {} for {} ({}).'.format(book_request.book.submitter.username,
                                                                      book_request.book.title,
                                                                      book_request.pk))

        # Scan all reports (create_related_niqati_codes) automatically
        # prevents replication.
        for report in Report.objects.filter(session__is_deleted=False):
            report.create_related_niqati_codes()
            self.stdout.write(u'Add niqati for {}.'.format(report))
