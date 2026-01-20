from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, DetailView, UpdateView
from ..models import Category, Author, Genre, Book, User
from ..forms import BookForm

def landing_page(request):
    return render(request, 'saybabook_app/landingpage.html')


class BookCreateView(LoginRequiredMixin, CreateView):
    form_class = BookForm
    template_name = 'saybabook_app/addbook.html'
    success_url = reverse_lazy('book.show')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() 
        context['authors'] = Author.objects.all() 
        context['genres'] = Genre.objects.all()
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user 
        self.object.save()
        form.save_m2m()
        new_authors_str = form.cleaned_data.get('new_authors')
        if new_authors_str:
            names = [n.strip() for n in new_authors_str.split(',') if n.strip()]
            for name in names:
                author_obj, _ = Author.objects.get_or_create(name=name)
                self.object.author.add(author_obj)
        new_genres_str = form.cleaned_data.get('new_genres')
        if new_genres_str:
            genres_list = [g.strip() for g in new_genres_str.split(',') if g.strip()]
            for g_name in genres_list:
                genre_obj, _ = Genre.objects.get_or_create(name=g_name)
                self.object.genres.add(genre_obj)

        return redirect(self.success_url)
    
class BookListView(ListView):
    model = Book
    template_name = 'saybabook_app/browse.html' 
    context_object_name = 'books' 
    def get_queryset(self):
        queryset = Book.objects.filter(book_privacy='public').order_by('-created_at').select_related(
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
        context['users'] = User.objects.all().values_list('username', flat=True)
        return context
    
class PrivateBookListView(ListView):
    model = Book
    template_name = 'saybabook_app/mybooks.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        queryset = Book.objects.filter(owner=self.request.user).order_by('-created_at').select_related(
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
        context['users'] = User.objects.all().values_list('username', flat=True)
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
        context ['users'] = User.objects.all().values_list('username', flat=True)
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

class BookEditView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'saybabook_app/editbook.html' 
    context_object_name = 'book'
    success_url = reverse_lazy('book.private.show') 

    def get_queryset(self):
        """
        A user can ONLY edit books where 
        they are the owner
        """
        return Book.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)