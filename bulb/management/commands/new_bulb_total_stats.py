import datetime
from django.core.management.base import BaseCommand

from bulb.models import Session, Book, Request, Membership
from django.utils import timezone


class Command(BaseCommand):
    help = "Notify users on session occurring tomorrow."

    def handle(self, *args, **options):
        # Datetime
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)

        membership_count = Membership.objects.filter(is_active=True, submission_date__lt=today).count()
        request_count = Request.objects.filter(submission_date__lt=today).count()
        book_count = Book.objects.filter(submission_date__lt=today, is_deleted=False).count()
        session_count = Session.objects.filter(submission_date__lt=today, is_deleted=False).count()

        stats = [today, book_count, request_count,
                 membership_count, session_count]

        stats_str = [str(i) for i in stats]

        print ", ".join(stats_str)
