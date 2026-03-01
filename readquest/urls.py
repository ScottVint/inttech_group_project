from django.urls import path
from readquest import views

app_name = 'readquest'

urlpatterns = [
    path('register/', views.land_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.index, name='index'),
]