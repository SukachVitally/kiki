from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from kiki import forms


@login_required
def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.data.get('username')
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username,
                    first_name=form.data.get('first_name'),
                    last_name=form.data.get('last_name'),
                    email=form.data.get('email'),
                    password=form.data.get('password')
                )
                return redirect('/login')
            form.add_error('username', 'User already exist')
    else:
        form = forms.RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})
