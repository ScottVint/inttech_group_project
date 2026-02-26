from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from readquest.forms import UserForm

# Create your views here.
def land_register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 1. check the passwords match
        if password != confirm_password:
            print("Error: Passwords do not match")
            return render(request, 'readquest/register.html', {'error': 'Passwords do not match. Please try again.'})

        # 2. check the password length
        if len(password) < 8:
            print("Error: Password too short")
            return render(request, 'readquest/register.html', {'error': 'Password must be at least 8 characters long.'})

        # 3. check the password complexity (at least one uppercase letter, one lowercase letter, and one digit)
        if user_form.is_valid():
            user = user_form.save(commit=False)

            user.set_password(user.password)

            user.save()

            return redirect(reverse('readquest:login'))
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'readquest/register.html', {'user_form': user_form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('readquest:register'))
            else:
                return HttpResponse("Your ReadQuest account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'readquest/login.html')
