from django.urls import path
from readquest import views


app_name = 'readquest'

urlpatterns = [
    path('', views.index, name='index'),
]