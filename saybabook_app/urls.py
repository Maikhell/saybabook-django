from django.urls import path
from . import views
from .views import BookCreateView, BookListView, PrivateBookListView

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('archive/', views.archive_page, name = 'archive'), 
    path('browse/', BookListView.as_view(), name ='book.show'),
    path('addbook/', BookCreateView.as_view(), name = 'book.add'),
    path('mybooks/', PrivateBookListView.as_view(), name ='mybooks')
]