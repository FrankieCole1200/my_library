from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random
from loans.models import Book
from django.http import Http404
from loans.forms import BookForm

from django.core.paginator import Paginator

from django.contrib import messages

from django.views import View

ITEMS_PER_PAGE = 25

# Create your views here.
def welcome(request):
    slogans = [
        "Having fun isn't hard when you've got a library card.",
        "Believe in your shelf.",
        "Libraries make shhh happen.",
        "Need a good read? We’ve got you covered.",
        "Check us out. And maybe one of our books too.",
        "Get a better read on the world."
    ]
    
    random_number = random.randint(0, len(slogans) - 1)

    context = {'slogan': slogans[random_number]}
    return render(request, 'welcome.html', context)

def books(request):
    allBooks = Book.objects.all().order_by('id') # gives us a list of books in the DB
    paginator = Paginator(allBooks, ITEMS_PER_PAGE)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)
    context = {'page_object': page_object}
    return render(request, 'books.html', context)


def get_book(request, book_id):
    try:
        requested_book = Book.objects.get(pk=book_id)
        context = {'book_id': book_id, 'requested_book': requested_book}
    except Book.DoesNotExist:
        raise Http404(f"Could not find book with primary key {book_id}")
    else:
        return render(request, 'get_book.html', context)
    

def get_bookv2(request, book_id):
    foo = request.GET.get('foo', 0)
    bar = request.GET.get('bar', 0)
    return HttpResponse(f"You're requesting book with book_id {book_id}, foo={foo}, bar{bar}")

class CreateBookView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'create_book.html', {'form': form})
    
    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "It was not possible to save this book")
            else:
                path = reverse('books')
                return HttpResponseRedirect(path)
        return render(request, 'create_book.html', {'form': form})



def update_book(request, book_id):
    # check if we have a valid book_id
    try:
        requested_book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist: # 404 error if the book id is non exisitent in the DB
        raise Http404(f"Could not find book with primary key {book_id}")
    
    # check to see if we have a POST request we want to update the existing Book in the DB
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=requested_book) # create a bounded form
        # check the form is valid
        if form.is_valid():
            try:
                book = form.save()
            except:
                form.add_error(None, "It was not possible to save this book")
            else:
                messages.info(request, f"Updated book record to: {book}")
                path = reverse('books')
                return HttpResponseRedirect(path)
    else: # if request is GET we need to show the form to the user
        form = BookForm(instance=requested_book) # show a form with filled in details about the chosen book
        context = {'book_id': book_id, 'form': form}
        return render(request, 'update_book.html', context)


def delete_book(request, book_id):
    # check if we have a valid book_id
    try:
        requested_book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist: # 404 error if the book id is non existent in the DB
        raise Http404(f"Could not find book with primary key {book_id}")
    
    if request.method == "POST":
        requested_book.delete()
        path = reverse('books')
        return HttpResponseRedirect(path)
    else:
        context = {'book_id': book_id, 'requested_book': requested_book}
        return render(request, 'delete_book.html', context)
