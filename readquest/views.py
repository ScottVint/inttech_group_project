from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from readquest.forms import UserForm, BookForm
from .models import Achievement
from .models import Book
from .models import ProgressRecord
from django.contrib.auth.decorators import login_required

from .services import search_books


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
    context_dict = {}
    context_dict['user'] = request.user #fetches the user that sent the request
    context_dict['achivements'] = Achievement.objects.filter(earners=request.user)
    context_dict['current_read'] = Book.objects.filter(currently_reading=request.user)

    return render(request, 'readquest/home.html', context=context_dict)

@login_required
def book_list(request):
    context_dict['read_books'] = Book.objects.filter(read_by=request.user)
    context_dict['wishlisted'] = Book.objects.filter(wishlisted_by=request.user)
    return render(request, 'readquest/home.html', context=context_dict)

@login_required
def profile(request):
    context_dict = {}
    context_dict['read_books'] = Book.objects.filter(read_by=request.user)
    context_dict['current_read'] = Book.objects.filter(currently_reading=request.user)
    context_dict['wishlisted'] = Book.objects.filter(wishlisted_by=request.user)
    context_dict['badges'] = Achievement.objects.filter(earners=request.user)
    return render(request, 'readquest/profile.html', context=context_dict)

@login_required
def finish_book(request, book_id):
    if request.method == 'POST':
        try:
            book = Book.objects.get(id=book_id)
            book.currently_reading.remove(request.user)
            book.read_by.add(request.user)
        except Book.DoesNotExist:
            pass
    return redirect(reverse('readquest:profile'))

@login_required
def add_to_currently_reading(request):
    if request.method == 'POST':
        ol_key = request.POST.get('ol_key', '').strip()
        title = request.POST.get('title', 'Unknown Title').strip()
        author = request.POST.get('author', 'Unknown Author').strip()
        pages = request.POST.get('pages', 0)
        cover_url = request.POST.get('cover_url', '').strip()

        try:
            pages = int(pages)
        except (ValueError, TypeError):
            pages = 0

        book, _ = Book.objects.get_or_create(
            ol_key=ol_key,
            defaults={
                'title': title,
                'author': author,
                'pages': pages,
                'cover_url': cover_url or None,
            }
        )
        book.currently_reading.add(request.user)

    return redirect(reverse('readquest:profile'))

@login_required
def goals(request):
    context_dict = {'progress_record': ProgressRecord.objects.filter(owner=request.user)}
    return render(request,'readquest/goals.html', context=context_dict)

@login_required
def catalogue(request):
    return render(request,'readquest/catalogue.html', context={'books': Book.objects.all()})
    
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
        book = details.parent

    except Detail.DoesNotExist:
        book = None

    except Book.DoesNotExist:
        book = None

    if book is None:
        return redirect('') # Where to redirect?

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
    return render(request, 'readquest/review.html', context=context_dict)

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save()
            book.currently_reading.add(request.user)
            return redirect(reverse('readquest:profile'))

        else:
            print(form.errors)

    return redirect(reverse('readquest:profile'))


def book_search(request):
    query = request.GET.get("q", "").strip()
    print("QUERY:", query)
    results = []
    
    if query:
        try: 
            results = search_books(query)
        except Exception as e:
            messages.error(request, "Please try again")
    return render(request, "readquest/book-search.html", {"results": results, "query": query})
