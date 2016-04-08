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
        for day in range(diff):
            date = bulb_start_date + datetime.timedelta(day)
            membership_count = Membership.objects.filter(is_active=True, submission_date__lt=date).count()
            request_count = Request.objects.filter(submission_date__lt=date).count()
            book_count = Book.objects.filter(submission_date__lt=date, is_deleted=False).count()
            session_count = Session.objects.filter(submission_date__lt=date, is_deleted=False).count()

            stats = [date, book_count, request_count,
                     membership_count, session_count]

            stats_str = [str(i) for i in stats]

            print ", ".join(stats_str)
