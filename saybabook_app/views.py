from django.shortcuts import render, redirect
from django.db.models import F
from .models import Category, Author, Genre, Book, User

def landing_page(request):
    return render(request, 'saybabook_app/landingpage.html')

def browse_page(request):
    return render(request, 'saybabook_app/browse.html')

def archive_page(request):
    return render (request, 'saybabook_app/archive.html')

def account_page(request):
    return render(request, 'saybabook_app/account.html')

def add_book_page(request):
    if request.method == 'POST':
        title = request.POST.get('bookTitle')
        author_id = request.POST.get('bookAuthor')
        privacy = request.POST.get('bookPrivacy')
        description = request.POST.get('bookDescription')
        status = request.POST.get('bookStatus')
        link = request.POST.get('bookOnlineLink')
        cover_file = request.FILES.get('bookCover')
        
        author_instance = Author.objects.get(id=author_id)
        
        new_book = Book.objects.create(
            book_title = title,
            book_description = description,
            book_status = status,
            book_cover = cover_file,
            book_privacy = privacy,
            book_online_link = link,
            author = author_instance
        )
        genre_ids = request.POST.getlist('bookGenre')
        new_book.genres.set(genre_ids)
        
        return redirect('book.show')
    else:
        context = {
            'authors': Author.objects.all(),
            'categories': Category.objects.all(),
            #Category id null?
            'genres': Genre.objects.all()
        }
        return render(request, 'saybabook_app/addbook.html', context)

def show_books(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    genres = Genre.objects.all()
    books = Book.objects.filter(book_privacy ='public').select_related('author').order_by('-created_at')
    #Make the retrieval specfic for names, dont use all()
    users= User.objects.all()
    context = {
        'categories': categories,
        'authors': authors,
        'genres': genres,
        'books' : books,
        'users' : users
    }
    
    return render(request, 'saybabook_app/browse.html', context)
