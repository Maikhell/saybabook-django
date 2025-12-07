from django.shortcuts import render, redirect 
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DeleteView, DetailView
from ..models import User
from ..forms import UserForm

class UserCreateView(CreateView):
    form_class = UserForm
    template_name = 'saybabook_app/landingpage.html'
    success_url = reverse_lazy('book.show')
    def add_book_fbv(request):
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = UserForm(request.POST, request.FILES) 

            # Check if the form is valid
            if form.is_valid():
                # SUCCESS: Data is good. Save the object.
                form.save()
                return redirect('book.show')
            else:
                # FAILURE: Data is bad. Form.errors contains the issues.
                # Drop through to render the page with the errors attached to the form.
                pass 
        
        # For GET request or failed POST request, render the template
        else:
            form = UserForm()
            
        # The template rendering below will display the form, including any errors
        return render(request, 'saybabook_app/landingpage.html', {'form': form})