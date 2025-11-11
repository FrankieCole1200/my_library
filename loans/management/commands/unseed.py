from loans.models import Book

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "This command removes all books from the database"

    def handle(self, *args, **options):
        books = Book.objects.all() 
        for book in books:
            book.delete()


