from django.shortcuts import render

# Create your views here.
def land_register(request):
    return render(request, 'readquest/land_register.html')