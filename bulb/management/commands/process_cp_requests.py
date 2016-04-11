import unicodecsv
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from bulb.models import Request, Book


class Command(BaseCommand):
    help = "Handle the requests received during the Cultural Program."

    def handle(self, *args, **options):
        cp_file = open('cp.csv')
        reader = unicodecsv.reader(cp_file, encoding="utf-8")
        borrowing_end_date = datetime.date(2016,5,1)
        for row in reader:
            username = row[0].lower()
            book_pk = int(row[1])
            status = row[2]

            user = User.objects.get(username=username)
            book = Book.objects.get(pk=book_pk)
            book.is_available = False
            book.save()

            book_request = Request.objects.create(requester=user,
                                                  book=book,
                                                  delivery='I',
                                                  status=status,
                                                  requester_status_date=timezone.now(),
                                                  requester_status=status,
                                                  owner_status_date=timezone.now(),
                                                  owner_status=status)

            if book.contribution == 'G':
                balance_test = user.book_points.count_total_giving
            elif book.contribution == 'L':
                balance_test = user.book_points.count_total_lending
                book_request.borrowing_end_date = borrowing_end_date
                book_request.save()

            book_request.create_related_points()
