from django.http import HttpResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import User


# Create your views here.
@csrf_protect
def home(request):
    return render(request, 'home.html')


def signin(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST['credential'],
                               password=request.POST['password']).exists() or User.objects.filter(
                email=request.POST['credential'], password=request.POST['password']).exists():
            return render(request, 'home.html')
        return render(request, 'login.html', {'error': 'Invalid details'})
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        form = {
            "username": request.POST['username'],
            "email": request.POST['email'],
            "pass1": request.POST['pass1'],
            "pass2": request.POST['pass2'],
        }
        if User.objects.filter(username=request.POST["username"]).exists():
            return render(request, 'signup.html', {"error":"Username exists", 'form_details':form})
        if User.objects.filter(email=request.POST["email"]).exists():
            return render(request, 'signup.html', {"error":"Email exists", 'form_details':form})
        if not request.POST['pass1'] == request.POST['pass2']:
            return render(request, 'signup.html', {"error":"Passwords don't match", 'form_details':form})
        new_user = User.objects.create(username=request.POST['username'], email=request.POST['email'],
                                       password=request.POST['pass1'])
        new_user.save()
        # redirect to login
        return render(request, 'login.html')
    return render(request, 'signup.html')


def signout(request):
    return render(request, 'login.html')
