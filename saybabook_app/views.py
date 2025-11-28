from django.shortcuts import render


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

