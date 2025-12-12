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

ProfileInlineFormSet = inlineformset_factory(
    parent_model=User,
    model=UserProfile,
    fields=['email', 'name', 'userImage'], # Fields from the UserProfile model
    can_delete=False, # We don't want the user to delete their profile
    extra=1,          # Allow one extra blank form if no profile exists
    max_num=1         # Limit to one profile per user (since it's a OneToOne)
)
class UserEditView(LoginRequiredMixin, UpdateView):
    model = User 
    fields = ['user_name'] # The fields for the primary User model
    template_name = 'saybabook_app/account.html'
    success_url = reverse_lazy('account.edit') 
    form_class = UserAccountForm # Use the simple UserAccountForm

    def get_object(self, queryset=None):
        """Always edit the currently logged-in user."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Pass the inline formset to the context."""
        context = super().get_context_data(**kwargs)
        
        if self.request.POST:
            # If POST, pass submitted data and files
            context['profile_formset'] = ProfileInlineFormSet(
                self.request.POST, 
                self.request.FILES, 
                instance=self.object
            )
        else:
            # If GET, pass existing instance
            context['profile_formset'] = ProfileInlineFormSet(instance=self.object)
            
        return context

    # 🔑 KEY FIX: Override form_valid to save the primary form AND the formset.
    def form_valid(self, form):
        # 1. Save the primary form (UserAccountForm)
        self.object = form.save()
        
        # 2. Get the profile formset from the context
        profile_formset = self.get_context_data()['profile_formset']
        
        # 3. Check if the formset is valid
        if profile_formset.is_valid():
            # 4. Save the formset—this saves or creates the related UserProfile instance
            profile_formset.instance = self.object # Ensure the formset knows which User to link to
            profile_formset.save()
            
        return super().form_valid(form) # Redirect to success_url
        
class UserDeleteView(DeleteView):
    form_class = UserAccountForm

