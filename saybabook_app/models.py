from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


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

User = get_user_model() 

class UserProfile(models.Model):
    # Link to the built-in User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    userImage = models.ImageField(upload_to='user_profile/', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This prevents errors if a user is saved but somehow doesn't have a profile
    if hasattr(instance, 'profile'):
        instance.profile.save()    
class Book(models.Model):
    #User FK 
    book_title = models.CharField(max_length=255, verbose_name='Title')
    book_description = models.TextField(blank=True, null=True, verbose_name='Description') 
    book_online_link = models.URLField(max_length=500, blank=True, null=True, verbose_name='Online Read Link')
    #Installed Pillow for Images
    book_cover = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name='Book Cover')
    book_privacy = models.TextField(blank=True, null=True, verbose_name='Privacy') 
    book_status = models.TextField(blank=True, null=True, verbose_name='Status') 
    #Book Genre Name Joined, like if its 1 and 2 its horror, drama
    book_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='books_added' )
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    author = models.ManyToManyField(Author,related_name='books', blank = True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title

