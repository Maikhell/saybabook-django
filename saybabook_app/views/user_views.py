from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import User, UserProfile
from ..forms import UserForm
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password

class UserCreateView(CreateView):
    form_class = UserForm
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
    #Need to change the model to specify the field and load the account tab
    model = User 
    
    # Specify the form fields you want to allow the user to edit
    fields = ['first_name', 'last_name', 'email', 'userimage'] 
    
    # Template where the edit form is rendered
    template_name = 'saybabook_app/account.html' 
    
    # Where to redirect the user after the form is successfully submitted
    success_url = reverse_lazy('account.edit') 

    # 🔑 KEY FIX: Override get_object to retrieve the currently logged-in user
    def get_object(self, queryset=None):
        return self.request.user

    # Optional: You can still add extra context data if needed, but 'users' is misleading.
    # If you need to access UserProfile, it should be done through the user object.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # You would access the current user's profile like this:
        context['user_profile'] = self.request.user.userprofile 
        return context
        
class UserDeleteView(DeleteView):
    form_class = UserForm

