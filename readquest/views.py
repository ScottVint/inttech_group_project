from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from readquest.forms import UserForm
import readquest.models
from django.contrib.auth.decorators import login_required

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
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks in seconds
                else:
                    request.session.set_expiry(0)  # expires when browser closes
                return redirect(reverse('readquest:home'))
            else:
                return HttpResponse("Your ReadQuest account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'readquest/login.html')

def index(request):

    return render(request,'readquest/index.html')


@login_required
def home(request):
    return render(request, 'readquest/home.html')

@login_required
def book_list(request):
    user_books = Book.objects.filter(user=request.user)

    return render(request, 'readquest/home.html', {'books': user_books})

@login_required
def profile(request):
    return render(request,'readquest/profile.html')

@login_required
def goals(request):
    return render(request,'readquest/goals.html')

@login_required
def catalogue(request):
    return render(request,'readquest/catalogue.html')
    
def show_details(request, details_slug):
    context_dict = {}

    try:
        details = Details.objects.get(slug=details_slug)
        book = details.objects.select_related('book').get()
        context_dict['details'] = details
        context_dict['book'] = book

    except Detail.DoesNotExist:
        context_dict['details'] = None
        context_dict['book'] = None

    except Book.DoesNotExist:
        context_dict['details'] = None
        context_dict['book'] = None

    return render(request, 'readquest/details.html', context=context_dict)

def book_review(request, details_slug):
    # Display details for book
    try:
        details = Details.objects.get(slug=details_slug)
        book = details.objects.select_related('book').get()

    except Detail.DoesNotExist:
        book = None

    except Book.DoesNotExist:
        book = None

    if book is None:
        return redirect('')

    form = ReviewForm()

    # Form submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if book:
                review = form.save()

            return redirect(reverse('readquest:details',
                                     kwargs={'details_slug':
                                             details_slug}))

    context_dict = {'form': form, 'book': book}
    return render(request, 'readquest/review.html', {'form': form})

            
