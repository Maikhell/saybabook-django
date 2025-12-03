from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Author Name')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    class Meta:
        verbose_name_plural = "Categories" 
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Genre Name')
    
    def __str__(self):
        return self.name

class Book(models.Model):
    book_title = models.CharField(max_length=255, verbose_name='Title')
    book_description = models.TextField(blank=True, null=True, verbose_name='Description') 
    book_online_link = models.URLField(max_length=500, blank=True, null=True, verbose_name='Online Read Link')
    #Installed Pillow for Images
    book_cover = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name='Book Cover')
    book_privacy = models.TextField(blank=True, null=True, verbose_name='Privacy') 
    book_status = models.TextField(blank=True, null=True, verbose_name='Status') 

    book_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    author = models.ManyToManyField(Author,related_name='books', blank = True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title

class UserProfile(models.Model):
    # For a real application, replace this with linking to Django's Auth User
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True,blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class User(models.Model):
    username = models.CharField(max_length=60, unique=True, verbose_name='Username') 
    password = models.CharField(max_length=128) # Passwords should use Hashing (min length 128)
    
    def __str__(self):
        return self.username