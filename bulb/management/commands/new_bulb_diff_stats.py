import datetime
from django.core.management.base import BaseCommand

from bulb.models import Session, Book, Request, Membership
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.now()
        today = datetime.datetime(now.year, now.month, now.day)
        last_week = today - datetime.timedelta(7)
        membership_diff = Membership.objects.filter(submission_date__gte=last_week, submission_date__lt=today, is_active=False).count()
        request_diff = Request.objects.filter(submission_date__gte=last_week, submission_date__lt=today).count()
        book_diff = Book.objects.filter(submission_date__gte=last_week, submission_date__lt=today, is_deleted=False).count()
        session_diff = Session.objects.filter(submission_date__gte=last_week, submission_date__lt=today, is_deleted=False).count()

        stats = [last_week, book_diff, request_diff,
                 membership_diff, session_diff]

        stats_str = [str(i) for i in stats]

        print ", ".join(stats_str)
