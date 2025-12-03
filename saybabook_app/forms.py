from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        #fields must be the same name of the forms
        fields = [
            'book_title', 
            'book_description', 
            'book_online_link', 
            'book_cover', 
            'book_privacy', 
            'book_status', 
            'book_category', 
            'genres', 
            'author' 
        ]
        
        #custom widgets
        widgets = {
            'book_description': forms.Textarea(attrs={'cols': 80, 'rows': 5})
        }