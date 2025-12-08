from django.urls import path
from .views import book_views, authenticate_views
from .views.book_views import BookCreateView, BookListView, PrivateBookListView, ArchivedBookListView, BookDeleteView
from .views.user_views import UserCreateView, UserEditView
urlpatterns = [
    path('', book_views.landing_page, name='home'),
    path('browse/', BookListView.as_view(), name ='book.show'),
    path('addbook/', BookCreateView.as_view(), name = 'book.add'),
    path('account/', UserEditView.as_view(), name = 'account.show'),
    path('mybooks/', PrivateBookListView.as_view(), name ='mybooks'),
    path('archive/', ArchivedBookListView.as_view(), name = 'book.archive.show'),
    path('mybooks/<int:pk>/delete', BookDeleteView.as_view(), name = 'book.delete'),
    path('landingpage/', UserCreateView.as_view(), name = 'user.create'),
    path('landingpage/', authenticate_views.user_logout, name = 'user.logout')
]