from django.urls import path
from . import views
from .views import BookCreateView, BookListView, PrivateBookListView, ArchivedBookListView, BookDeleteView

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('browse/', BookListView.as_view(), name ='book.show'),
    path('addbook/', BookCreateView.as_view(), name = 'book.add'),
    path('mybooks/', PrivateBookListView.as_view(), name ='mybooks'),
    path('archive/', ArchivedBookListView.as_view(), name = 'book.archive.show'),
    path('mybooks/<int:pk>/delete', BookDeleteView.as_view(), name = 'book.delete')
]