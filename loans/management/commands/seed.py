from loans.models import Book
from faker import Faker

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "This command adds 100 randomly generated books to the database (not real books)"

    def handle(self, *args, **options):
        fake = Faker()

        for i in range(0, 100):
            Book.objects.create(
                authors=fake.name(),
                title=fake.sentence(nb_words=4),
                publication_date=fake.date(),
                isbn=fake.unique.isbn10()
            )
        

