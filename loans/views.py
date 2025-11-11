from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random
from loans.models import Book
from django.http import Http404
from loans.forms import BookForm

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
    allBooks = Book.objects.all() # gives us a list of books in the DB
    context = {'books': allBooks}
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


def create_book(request):
    # checks to see if the request is a POST request which means we are recieving a form from the browser
    if request.method == "POST":
        form = BookForm(request.POST)
        # make sure all the data is of the correct type
        # if it is invalid the code skips to the end and we show another blank form but this time with error messages
        if form.is_valid():
            # save the book to the DB#
            try:
                form.save()
            except:
                form.add_error(None, "It was not possible to save this book")
            else:
                path = reverse('books')
                return HttpResponseRedirect(path)
    else: # if the request is a GET request which means the user wants to enter a form
        form = BookForm() # display a blank form
    return render(request, 'create_book.html', {'form': form})


def update_book(request, book_id):
    # check if we have a valid book_id
    try:
        requested_book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist: # 404 error if the book id is non exisitent in the DB
        raise Http404(f"Could not find book with primary key {book_id}")
    
    # check to see if we have a POST request we want to update the existing Book in the DB
    if request.method == "POST":
        form = BookForm(request.POST, instance=requested_book) # create a bounded form
        # check the form is valid
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "It was not possible to save this book")
            else:
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
    except Book.DoesNotExist: # 404 error if the book id is non exisitent in the DB
        raise Http404(f"Could not find book with primary key {book_id}")
    
    if request.method == "POST":
        requested_book.delete()
        path = reverse('books')
        return HttpResponseRedirect(path)
    else:
        context = {'book_id': book_id, 'requested_book': requested_book}
        return render(request, 'delete_book.html', context)
