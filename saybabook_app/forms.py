from django import forms
from .models import Book , User, UserProfile


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
class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name'] 
        # Note: We do not include the user_profile field here.

# 2. Form for the UserProfile model (Child)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'name', 'userImage']
        
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )