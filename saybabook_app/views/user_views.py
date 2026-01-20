from django.shortcuts import redirect 
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import User, UserProfile
from ..forms import UserAccountForm, UserProfileForm
from django.contrib.auth import login
from django.db import transaction
from ..forms import UserRegisterForm 

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'saybabook_app/landingpage.html'
    success_url = reverse_lazy('book.show')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserAccountForm
    template_name = 'saybabook_app/account.html'
    success_url = reverse_lazy('account.edit') 

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = context.get('form')
        
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        
        if self.request.POST:
            context['profile_form'] = UserProfileForm(
                self.request.POST, 
                self.request.FILES, 
                instance=user_profile
            )
        else:
            context['profile_form'] = UserProfileForm(instance=user_profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserAccountForm(request.POST, instance=self.object)
        user_profile, _ = UserProfile.objects.get_or_create(user=self.object)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=user_form, profile_form=profile_form)
            )
class UserDeleteView(DeleteView):
    form_class = UserAccountForm

