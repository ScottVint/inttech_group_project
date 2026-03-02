import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'inttech_group_project.settings',
                      )

import django
django.setup()

from django.contrib.auth.models import User
from readquest.models import Userpage, Book, Details, ProgressRecord, Achievement
import random

random.seed(67)


def populate():
    # --- Users (5) ---
    users = [
        add_user('alice',   'alice@123.org',   'alicepassword'),
        add_user('bob',     'bob@123.org',     'bobpassword'),
        add_user('charlie', 'charlie@123.org', 'charliepassword'),
        add_user('deborah', 'deborah@123.org', 'deborahpassword'),
        add_user('ethan',   'ethan@123.org',   'ethanpassword'),
    ]

    # --- Userpages (5, one per user) ---
    for user in users:
        add_userpage(user,
                     views=random.randint(0, 9999),
                     likes=random.randint(0, 9999))

    # --- Books (5) ---
    # NOTE: cover_image left blank — please upload images manually via the admin panel.
    books = [
        add_book(isbn=9780747532699,
                 title="Harry Potter and the Philosopher's Stone",
                 author='J.K. Rowling',
                 pages=223,
                 blurb='A young boy discovers he is a wizard and is invited to study at Hogwarts.'),

        add_book(isbn=9780261102217,
                 title='The Lord of the Rings',
                 author='J.R.R. Tolkien',
                 pages=1178,
                 blurb='An epic quest to destroy the One Ring and defeat the Dark Lord Sauron.'),

        add_book(isbn=9780451524935,
                 title='1984',
                 author='George Orwell',
                 pages=328,
                 blurb='A dystopian novel set in a totalitarian society ruled by Big Brother.'),

        add_book(isbn=9780743273565,
                 title='The Great Gatsby',
                 author='F. Scott Fitzgerald',
                 pages=180,
                 blurb='A story of wealth, love, and the American Dream set in the Jazz Age.'),

        add_book(isbn=9780062316097,
                 title='The Alchemist',
                 author='Paulo Coelho',
                 pages=208,
                 blurb='A philosophical novel about a shepherd on a journey to find worldly treasure.'),
    ]

    # --- Details (5, one per book) ---
    add_details(books[0], favourites=320, reads=1500)
    add_details(books[1], favourites=210, reads=980)
    add_details(books[2], favourites=450, reads=2100)
    add_details(books[3], favourites=175, reads=760)
    add_details(books[4], favourites=390, reads=1300)

    # --- ProgressRecords (5) ---
    add_progress(owner=users[0], name='alice-hp',      book=books[0], stage_current=5,  stage_final=17)
    add_progress(owner=users[1], name='bob-lotr',      book=books[1], stage_current=12, stage_final=62)
    add_progress(owner=users[2], name='charlie-1984',  book=books[2], stage_current=8,  stage_final=23)
    add_progress(owner=users[3], name='deborah-gatsby', book=books[3], stage_current=9, stage_final=9)
    add_progress(owner=users[4], name='ethan-alchemist', book=books[4], stage_current=3, stage_final=15)

    # --- Achievements (5) ---
    # NOTE: icon left blank — please upload images manually via the admin panel.
    add_achievement('Bookworm',       [users[0], users[1]])
    add_achievement('Speed Reader',   [users[2]])
    add_achievement('First Chapter',  [users[0], users[2], users[3]])
    add_achievement('Page Turner',    [users[1], users[4]])
    add_achievement('Finish Line',    [users[3]])

    # --- Wishlist / Read relationships ---
    books[0].wishlisted_by.add(users[1], users[2])
    books[1].wishlisted_by.add(users[0], users[3])
    books[2].read_by.add(users[0], users[1])
    books[3].read_by.add(users[2], users[4])
    books[4].read_by.add(users[3])

    print('Database populated successfully!')
    print(f'  Users:           {User.objects.count()}')
    print(f'  Userpages:       {Userpage.objects.count()}')
    print(f'  Books:           {Book.objects.count()}')
    print(f'  Details:         {Details.objects.count()}')
    print(f'  ProgressRecords: {ProgressRecord.objects.count()}')
    print(f'  Achievements:    {Achievement.objects.count()}')


def add_user(username, email, password):
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.email = email
        user.set_password(password)
        user.save()
    return user


def add_userpage(user, views=0, likes=0):
    up, created = Userpage.objects.get_or_create(owner=user)
    up.views = views
    up.likes = likes
    up.save()
    return up


def add_book(isbn, title, author, pages, blurb):
    # cover_image is left blank — upload manually via the admin panel
    b, created = Book.objects.get_or_create(isbn=isbn, defaults={
        'title': title,
        'author': author,
        'pages': pages,
        'blurb': blurb,
    })
    if not created:
        b.title = title
        b.author = author
        b.pages = pages
        b.blurb = blurb
        b.save()
    return b


def add_details(book, favourites, reads):
    d, created = Details.objects.get_or_create(book=book, defaults={
        'favourites': favourites,
        'reads': reads,
    })
    if not created:
        d.favourites = favourites
        d.reads = reads
        d.save()
    return d


def add_progress(owner, name, book, stage_current, stage_final):
    p, created = ProgressRecord.objects.get_or_create(name=name, defaults={
        'owner': owner,
        'book': book,
        'stage_current': stage_current,
        'stage_final': stage_final,
    })
    if not created:
        p.owner = owner
        p.book = book
        p.stage_current = stage_current
        p.stage_final = stage_final
        p.save()
    return p


def add_achievement(name, earners):
    # icon is left blank — upload manually via the admin panel
    a, created = Achievement.objects.get_or_create(name=name)
    for user in earners:
        a.earners.add(user)
    a.save()
    return a


if __name__ == '__main__':
    print('Starting ReadQuest population script...')
    populate()