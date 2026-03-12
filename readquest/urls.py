from django.urls import path
from readquest import views

app_name = 'readquest'

urlpatterns = [
    path('register/', views.land_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('goals', views.goals, name='goals'),
    path('catalogue', views.catalogue, name='catalogue'),
]