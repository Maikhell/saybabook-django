from django import forms
from .models import Book , User, UserProfile, Author, Genre
from django.contrib.auth.forms import UserCreationForm

class BookForm(forms.ModelForm):
    new_authors = forms.CharField(
        required=False, 
        help_text="Separate multiple authors with commas",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. J.K. Rowling, George Orwell'})
    )
    new_genres = forms.CharField(
        required=False, 
        help_text="Separate multiple genres with commas",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sci-Fi, Mystery'})
    )

    class Meta:
        model = Book
        fields = [
            'book_title', 'book_description', 'book_online_link', 
            'book_cover', 'book_privacy', 'book_status', 
            'book_category', 'genres', 'author' 
        ]
        widgets = {
            'book_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    fields = UserCreationForm.Meta.fields + ('email',)        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['userImage', 'name']
        
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
