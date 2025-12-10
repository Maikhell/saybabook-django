from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from ..models import User, UserProfile
from ..forms import LoginForm
from django.contrib.auth import logout,  authenticate, login
from django.contrib.auth.hashers import make_password

def user_logout(request):
    logout(request)
    return redirect('landingpage')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) # Initialize form with POST data
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #  KEY STEP 1: Check credentials against the database
            user = authenticate(request, username=username, password= password)
            if user is not None:
                #  KEY STEP 2: Log the user in and establish the session
                login(request, user)
                # Redirect to the page the user was trying to access, or a default
                next_url = request.GET.get('book.show')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('book.show') # Replace with your post-login page
            else:
                # Authentication failed
                # You can add an error message to the form here
                return render(request, 'saybabook_app/landingpage.html', {'form': form, 'error_message': 'Invalid credentials.'})
    else:
        # GET request: Display the empty form
        form = LoginForm()
        
    return render(request, 'saybabook_app/landingpage.html', {'form': form})