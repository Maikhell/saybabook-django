from django.contrib import admin
from.models import Author, Category, Genre, Book, UserProfile

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(UserProfile)

