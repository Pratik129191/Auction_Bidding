from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login, authenticate
from django.urls import reverse
from core.forms import CustomRegisterForm


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = CustomRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('system:home')
        else:
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('system:home')
