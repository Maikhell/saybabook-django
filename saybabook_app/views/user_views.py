from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView
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
    
class UserEditView(ListView):
    model = User
    template_name = 'saybabook_app/account.html'
    def get_queryset(self):
        query_set = User.objects.all().prefetch_related(
            'name', 'email','userimage'
        )
        return query_set
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['users'] = UserProfile.objects.all()
        return context
        
class UserDeleteView(DeleteView):
    form_class = UserForm

