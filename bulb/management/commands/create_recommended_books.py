from django.core.management.base import BaseCommand
from bulb.models import Book, RecommendedBook

class Command(BaseCommand):
    help = "Create RecommendedBook instances from Books."

    def handle(self, *args, **options):
        for book in Book.objects.iterator():
            if RecommendedBook.objects.filter(title=book.title.strip()).exists():
                continue
            print book.title
            recommend_book = RecommendedBook.objects.create(title=book.title,
                                                            category=book.category,
                                                            authors=book.authors)
            recommend_book.cover.name = book.cover.name
            recommend_book.save()
