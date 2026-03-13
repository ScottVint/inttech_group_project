from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from readquest.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from readquest.models import Book, ProgressRecord
import requests
import json

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
    current_reads = ProgressRecord.objects.filter(owner=request.user).order_by('-id')
    return render(request, 'readquest/profile.html', {'current_reads': current_reads})

@login_required
def search_books(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({'results': []})

    try:
        response = requests.get(
            'https://openlibrary.org/search.json',
            params={'title': query, 'limit': 5, 'fields': 'title,author_name,number_of_pages_median,isbn'},
            timeout=10
        )
        docs = response.json().get('docs', [])
    except requests.RequestException:
        return JsonResponse({'results': []})

    results = []
    for doc in docs:
        isbn_list = doc.get('isbn', [])
        isbn = isbn_list[0] if isbn_list else None
        results.append({
            'title': doc.get('title', 'Unknown'),
            'author': doc.get('author_name', ['Unknown'])[0] if doc.get('author_name') else 'Unknown',
            'pages': doc.get('number_of_pages_median') or 0,
            'isbn': isbn,
            'cover_url': f'https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg' if isbn else None,
        })

    return JsonResponse({'results': results})

@login_required
def add_book(request):
    if request.method != 'POST':
        return JsonResponse({'success': False})

    data = json.loads(request.body)
    isbn = data.get('isbn')
    title = data.get('title', 'Unknown')
    author = data.get('author', 'Unknown')
    pages = int(data.get('pages') or 1)

    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={'title': title, 'author': author, 'pages': pages, 'blurb': ''}
    )

    if created or not book.cover_image:
        try:
            resp = requests.get(f'https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg', timeout=10)
            if resp.status_code == 200 and len(resp.content) > 1000:
                book.cover_image.save(f'{isbn}.jpg', ContentFile(resp.content), save=True)
        except requests.RequestException:
            pass

    record_name = f'{request.user.username}-{isbn}'
    record, _ = ProgressRecord.objects.get_or_create(
        name=record_name,
        defaults={'owner': request.user, 'book': book, 'stage_current': 0, 'stage_final': pages}
    )

    return JsonResponse({'success': True})

@login_required
def goals(request):
    return render(request,'readquest/goals.html')

@login_required
def catalogue(request):
    return render(request,'readquest/catalogue.html')