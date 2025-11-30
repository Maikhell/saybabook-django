from django.shortcuts import render
from .models import Category, Author, Genre, Book, User

def landing_page(request):
    return render(request, 'saybabook_app/landingpage.html')

def browse_page(request):
    return render(request, 'saybabook_app/browse.html')

def archive_page(request):
    return render (request, 'saybabook_app/archive.html')

def add_book_page(request):
    return render(request, 'saybabook_app/addbook.html')

def account_page(request):
    return render(request, 'saybabook_app/account.html')

def create(request):
    return render(request, '', {'form'})

def show_books(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    genres = Genre.objects.all()
    books = Book.objects.filter(book_privacy ='public').select_related('author').order_by('-created_at')
    #Make the retrieval specfic for names, dont use all()
    users= User.objects.filter(username = 'Mai')
    context = {
        'categories': categories,
        'authors': authors,
        'genres': genres,
        'books' : books,
        'users' : users
    }
    
    return render(request, 'saybabook_app/browse.html', context)
