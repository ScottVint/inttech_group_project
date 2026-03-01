import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'inttech_group_project.settings',
                      )

import django
django.setup()
from readquest.models import *
import random

random.seed(67)

def populate():
    ### USER VALUES ###
    users = {'Alice' :
             {'name' : 'alice',
              'email' : 'alice@123.org',
              'password' : 'alicepassword',
              },

             'Bob' :
              {'name' : 'bob',
                'email' : 'bob@123.org',
                'password' : 'bobpassword',
                },
             
             'Charlie':
              {'name' : 'charlie',
                'email ' : 'charlie@123.org',
                'password' : 'charliepassword',
                },

             'Deborah':
              {'name' : 'deborah',
                'email' : 'deborah@123.org',
                'password' : 'alicepassword',
              },

             'Ethan':
              {'name' : 'ethan',
                'email' : 'ethan@123.org',
                'password' : 'ethanpassword',
              },

             'Fiona':
              {'name' : 'fiona',
                'email' : 'fiona@123.org',
                'password' : 'fionapassword',
              },

             'Gloria':
              {'name' : 'gloria',
                'email' : 'gloria@123.org',
                'password' : 'gloriapassword'
              },
             'Henry':
              {'name' : 'henry',
                'email' : 'henry@123.org',
                'password' : 'henrypassword',
              },
    }
    
    ### USERPAGE VALUES ###
    userpages = {'Alice': {'owner': users['Alice'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },
                
                 'Bob': {'owner': users['Bob'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },
                
                 'Charlie': {'owner': users['Charlie'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },
                
                 'Deborah': {'owner': users['Deborah'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },
                
                 'Ethan': {'owner': users['Ethan'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },

                 'Fiona': {'owner': users['Fiona'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },

                 'Gloria': {'owner': users['Gloria'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },

                 'Henry': {'owner': users['Henry'],
                           'views': random.randint(0,9999),
                           'likes': random.randint(0,9999),
                            },
                }
    
    for page, page_data in userpages.items():
        up = add_userpage(page, views=page_data['views'], likes=page_data['likes'])

    for up in Userpage.objects.all():
        print(f'- {up}')            
    # for cat, cat_data in cats.items():
    #     # Passes each item in cats into 
    #     c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
    #     for p in cat_data['pages']:
    #         add_page(c, p['title'], p['url'],p['views'])

    # for c in Category.objects.all():
    #     for p in Page.objects.filter(category=c):
    #         print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    # Finds or creates object with the given name.
    c = Category.objects.get_or_create(name=name)[0]

    # Passes views and likes to the corresponding attributes of Category (in models.py)
    c.views = views
    c.likes = likes
    c.save()
    return c
    
def add_user(name, email, password):
    try:
        User.objects.get(username=name)
    except:
        u = User.objects.create_user(name=name, email=email, password=password)[0]
    
    u.save()
    return u

def add_userpage(owner, views=0, likes=0):
    u = Userpage.objects.get_or_create(owner=owner)[0]
    u.views = views
    u.likes = likes
    u.save()
    return u


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()