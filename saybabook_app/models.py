from django.db import models

class Author(models.Model):
    # authorId is created automatically by Django (pk)
    full_name = models.CharField(max_length=150, unique=True, verbose_name='Author Name')
    def __str__(self):
        return self.full_name

class Category(models.Model):
    # categoryId is created automatically by Django (pk)
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')
    class Meta:
        verbose_name_plural = "Categories" # Fixes display in admin panel
    def __str__(self):
        return self.name

class Genre(models.Model):
    # genreId is created automatically by Django (pk)
    name = models.CharField(max_length=100, unique=True, verbose_name='Genre Name')
    
    def __str__(self):
        return self.name

# --- Book Model (With Relationships) ---

class Book(models.Model):
    # bookId is created automatically by Django (pk)
    book_title = models.CharField(max_length=255, verbose_name='Title')
    book_description = models.TextField(blank=True, null=True, verbose_name='Description') 
    book_online_link = models.URLField(max_length=500, blank=True, null=True, verbose_name='Online Read Link')
    book_cover = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name='Book Cover')
    book_privacy = models.TextField(blank=True, null=True, verbose_name='Privacy') 
    book_status = models.TextField(blank=True, null=True, verbose_name='Status') 

    #FK
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True,related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    
    # Many-to-Many field for genres (A book can have many genres, a genre can have many books)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)

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