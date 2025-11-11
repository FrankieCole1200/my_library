import django
from django.db import models

# Create your models here.
class Book (models.Model):
    authors = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    # override the method to convert our object to a string when printed out.
    def __str__(self):
        return(f"{self.authors}  ({self.publication_date.year})  \"{self.title}\" ISBN {self.isbn}.")
