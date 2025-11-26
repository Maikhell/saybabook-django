from django.db import models

class User(models.Model):
    username = models.CharField('Username', max_length=60)
    password = models.CharField('Password', max_length=30)
    email = models.EmailField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Book(models.Model):
    book_title = models.CharField('')
    book_author = models.CharField('')
    book_description = models.CharField('')
    book_category = models.CharField('')
    book_genre = models.CharField('')
    #Link may not be charfield change later
    book_online_link = models.CharField('')
    #Maybe the uploads/ might direct to a route
    book_cover = models.ImageField(upload_to='uploads/')
    
    
    
    
    
