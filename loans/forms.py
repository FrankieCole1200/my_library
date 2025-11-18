from django import forms

from loans.models import Book

# this is very similar to defining a model
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['image', 'authors', 'title', 'publication_date', 'isbn']
