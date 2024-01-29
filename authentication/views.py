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
        return HttpResponse("Invalid details")
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST["username"]).exists():
            return HttpResponse("username exists")
        if User.objects.filter(email=request.POST["email"]).exists():
            return HttpResponse("Email exists")
        if not request.POST['pass1'] == request.POST['pass1']:
            return HttpResponse("Passwords don't match")
        new_user = User.objects.create(username=request.POST['username'], email=request.POST['email'],
                                       password=request.POST['pass1'])
        new_user.save()
        return HttpResponse("Successful registration")
    return render(request, 'signup.html')


def signout(request):
    return render(request, 'login.html')
