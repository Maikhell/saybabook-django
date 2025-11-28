from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('browse/', views.browse_page, name ='browse'),
    path('addbook/', views.add_book_page, name = 'addbooks'),
    path('archive/', views.archive_page, name = 'archive')
]