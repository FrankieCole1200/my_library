import django
from django.db import models

# Create your models here.
class Book (models.Model):
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    authors = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)

    # override the method to convert our object to a string when printed out.
    def __str__(self):
        return(f"{self.authors}  ({self.publication_date.year})  \"{self.title}\" ISBN {self.isbn}.")

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return(f"Member {self.id}: {self.last_name}, {self.first_name} <{self.email}>")
    
class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    start_at = models.DateField()
    end_at = models.DateField()