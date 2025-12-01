from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('browse/', views.show_books, name ='book.show'),
    path('addbook/', views.add_book_page, name = 'book.add'),
    path('archive/', views.archive_page, name = 'archive')
]