from django.urls import path
# Assuming you set up __init__.py to import everything, or you import modules:
from .views import book_views, user_views, authenticate_views 

urlpatterns = [
    # --- Landing Page ---
    # Good use of bare path for the application root
    path('', book_views.landing_page, name='landingpage'),
    
    # --- Authentication (Ensure paths are unique!) ---
    path('register/', user_views.UserCreateView.as_view(), name='user.create'),
    path('login/' ,  authenticate_views.user_login, name = 'user.login' ),
    path('logout/', authenticate_views.user_logout, name='user.logout'),
    
    # --- Book Views ---
    path('browse/', book_views.BookListView.as_view(), name='book.show'),
    path('addbook/', book_views.BookCreateView.as_view(), name='book.add'),
    path('mybooks/', book_views.PrivateBookListView.as_view(), name='book.private.show'),
    path('archive/', book_views.ArchivedBookListView.as_view(), name='book.archive.show'),
    
    # --- Detail/Action Views ---
    path('mybooks/<int:pk>/delete/', book_views.BookDeleteView.as_view(), name='book.delete'),
    path('mybooks/<int:pk>/detail/', book_views.BookDetailView.as_view(), name = 'book.detail'),
    path('book/edit/<int:pk>/', book_views.BookEditView.as_view(), name='book.edit'),
    # --- Account Views ---
    path('account/edit/', user_views.UserEditView.as_view(), name='account.edit'),]
