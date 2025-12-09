from django.shortcuts import redirect 
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from ..models import User, UserProfile
from ..forms import UserForm
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('landingpage')