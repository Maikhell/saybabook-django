from django.shortcuts import redirect, render
from ..forms import LoginForm
from django.contrib.auth import logout,  authenticate, login

def user_logout(request):
    logout(request)
    return redirect('landingpage')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('book.show')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('book.show')
            else:
                return render(request, 'saybabook_app/landingpage.html', {'form': form, 'error_message': 'Invalid credentials.'})
    else:
        form = LoginForm()
        
    return render(request, 'saybabook_app/landingpage.html', {'form': form})