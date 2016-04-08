import datetime
from django.core.management.base import BaseCommand

from bulb.models import Session, Book, Request, Membership
from django.utils import timezone


class Command(BaseCommand):
    help = "Notify users on session occurring tomorrow."

    def handle(self, *args, **options):
        # Datetime
        current_date = datetime.datetime.now()
        bulb_start_date = datetime.datetime(2015, 10, 1)
        diff = (current_date - bulb_start_date).days
        for days in range(0, diff, 7):
            start_datetime = bulb_start_date + datetime.timedelta(days)
            end_datetime = bulb_start_date + datetime.timedelta(days + 7)
            membership_diff = Membership.objects.filter(submission_date__gte=start_datetime, submission_date__lt=end_datetime, is_active=True).count()
            request_diff = Request.objects.filter(submission_date__gte=start_datetime, submission_date__lt=end_datetime).count()
            book_diff = Book.objects.filter(submission_date__gte=start_datetime, submission_date__lt=end_datetime, is_deleted=False).count()
            session_diff = Session.objects.filter(submission_date__gte=start_datetime, submission_date__lt=end_datetime, is_deleted=False).count()

            stats = [start_datetime, book_diff, request_diff,
                     membership_diff, session_diff]

            stats_str = [str(i) for i in stats]

            print ", ".join(stats_str)
