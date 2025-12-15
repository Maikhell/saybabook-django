from django.shortcuts import render, redirect 
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import User, UserProfile
from ..forms import UserAccountForm, UserProfileForm
from django.contrib.auth import login
from django.forms.models import inlineformset_factory
from django.contrib.auth.hashers import make_password
from django.db import transaction

class UserCreateView(CreateView):
    form_class = UserAccountForm
    template_name = 'saybabook_app/landingpage.html'
    success_url = reverse_lazy('book.show')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        plain_password = form.cleaned_data.get('user_password')
        # Use make_password to hash the password
        user.user_password = make_password(plain_password)
        user.save()
        login(self.request, user)
        return super().form_valid(form)

class UserEditView(LoginRequiredMixin, UpdateView):
    # # The primary model remains User
    form_class = UserAccountForm
    model = User 
    template_name = 'saybabook_app/account.html'
    success_url = reverse_lazy('account.edit') 

    def get_object(self, queryset=None):
        """Always edit the currently logged-in user."""
        return self.request.user

    # Get initial data for the UserProfileForm
    def get_initial(self):
        initial = super().get_initial()
        user = self.get_object()
        
        # Pre-populate UserProfileForm fields if a UserProfile exists
        if hasattr(user, 'profile'):
            initial['userImage'] = user.profile.userImage
            initial['name'] = user.profile.name
            initial['email'] = user.profile.email
        
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        # Instantiate the UserProfileForm
        if self.request.POST:
            # If POST, pass submitted data and files
            context['profile_form'] = UserProfileForm(
                self.request.POST, 
                self.request.FILES, 
                instance=user.user_profile # Pass existing instance
            )
        else:
            user_profile, created = UserProfile.objects.get_or_create(profile_user=user)
            context['profile_form'] = UserProfileForm(instance=user_profile)
            
        # The user_form is already added by UpdateView as 'form'
        # We rename it in context for clarity in the template (account.html)
        context['user_form'] = context.pop('form')
        
        # Also pass the user_profile instance to display the current image
        context['user_profile'] = user.profile
            
        return context

    def form_valid(self, form):
        # 1. Save the primary User form
        self.object = form.save()
        
        # 2. Get the UserProfileForm from context (which was instantiated in get_context_data)
        profile_form = self.get_context_data(object=self.object)['profile_form']
        
        # 3. Check if the UserProfileForm is valid
        if profile_form.is_valid():
            # Create/Retrieve the UserProfile instance linked to the current User
            profile, created = UserProfile.objects.get_or_create(userProfile=self.object)
            
            # Update the form instance to be the one related to the user
            profile_form.instance = profile
            
            # 4. Save the UserProfile form
            profile_form.save()
            
        # 5. Redirect to success_url
        return super().form_valid(form)
        
class UserDeleteView(DeleteView):
    form_class = UserAccountForm

