from django.shortcuts import render, redirect 
from django.db.models import F
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import View, ListView, CreateView, DeleteView, DetailView
from ..models import Category, Author, Genre, Book, User
from ..forms import BookForm

def landing_page(request):
    return render(request, 'saybabook_app/landingpage.html')


class BookCreateView(LoginRequiredMixin,CreateView):
    #Owner Id is not saving need fix

    #user the book model
    form_class = BookForm
    #specify template to render the form
    template_name = 'saybabook_app/addbook.html'
    # reverse_lazy is used to look up the URL name once Django is fully initialized
    success_url = reverse_lazy('book.show')
    
    def form_valid(self, form):
    # Example: Assign the currently logged-in user to the book before saving
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        self.object = None
        context = super().get_context_data(**kwargs)
        # and Many-to-Many fields automatically in its select inputs!
        context['users'] = self.request.user.userprofile
        context['categories'] = Category.objects.all() 
        context['genres'] = Genre.objects.all()
        return context
    
    # Optional: Override the form_valid method to assign the user/extra logic
    
class BookListView(ListView):
    # 1. Which model to list
    model = Book
    #need fix here
    # 2. Template to render the list
    template_name = 'saybabook_app/browse.html' 
    # 3. Name for the list of objects in the template (was 'books')
    context_object_name = 'books' 
    
    # 4. Define the queryset to fetch data (with optimizations)
    def get_queryset(self):
        # to prevent N+1 queries when accessing related data in the template.
        queryset = Book.objects.filter(book_privacy='public').order_by('-created_at').select_related(
            'book_category' # ForeignKey lookup (one query)
        ).prefetch_related(
            'author', 'genres' # ManyToMany lookup (one query per M2M field)
        )
        return queryset

    # 5. Add extra context (categories, authors, genres, users) to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        # Ensure 'users' is handled correctly (assuming User is a simple model like yours)
        context['users'] = User.objects.all().values_list('user_name', flat=True)
        return context
    
    #Same as Above Just Retrieving Privates
class PrivateBookListView(ListView):
    model = Book
    template_name = 'saybabook_app/mybooks.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        # Note: filter by the currently logged-in user here
        queryset = Book.objects.filter(book_privacy='private').order_by('-created_at').select_related(
            'book_category'
        ).prefetch_related(
            'author', 'genres'
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        context['users'] = User.objects.all().values_list('user_name', flat=True)
        return context
    
class ArchivedBookListView(ListView):
    model = Book
    template_name = 'saybabook_app/archive.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        queryset = Book.objects.filter(book_status = 'archived').order_by('-created_at').select_related(
            'book_category'
        ).prefetch_related(
            'author', 'genres'
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['categories'] = Category.objects.all()
        context ['authors'] = Author.objects.all()
        context ['genres'] = Genre.objects.all()
        context ['users'] = User.objects.all().values_list('user_name', flat=True)
        return context
class BookDeleteView(DeleteView):
        model = Book
        template_name = 'saybabook_app/deletebook.html'
        success_url = reverse_lazy('book.show')
        
class BookDetailView(DetailView):
        model = Book
        template_name = 'saybabook_app/components/bookdetails.html'
        context_object_name = 'book'
        def dispatch(self, request, *args, **kwargs):
            
             return super().dispatch(request, *args, **kwargs)