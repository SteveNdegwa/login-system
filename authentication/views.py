from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from .forms import SigninForm, SignupForm


# Create your views here.
@csrf_protect
def home(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/home.html', {"name": request.user.username})
    else:
        return render(request, 'authentication/home.html')


def signin(request):
    # POST request
    if request.method == "POST":
        print(request.POST)
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                return render(request, 'authentication/signin.html', {'error': 'Incorrect username or password', 'form': form})
        else:
            return render(request, 'authentication/signin.html', {'error': 'Invalid details', 'form': form})

    # GET request
    else:
        form = SigninForm()
        return render(request, 'authentication/signin.html', {'form': form})


def signup(request):
    # POST request
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if User.objects.filter(username=username).exists():
                return render(request, 'authentication/signup.html', {"error": "Username exists", 'form': form})
            if User.objects.filter(email=email).exists():
                return render(request, 'authentication/signup.html', {"error": "Email exists", 'form': form})
            if not password == password2:
                return render(request, 'authentication/signup.html', {"error": "Passwords don't match", 'form': form})

            new_user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            new_user.save()
            return redirect("/signin/")

    # GET request
    else:
        form = SignupForm()
        return render(request, 'authentication/signup.html', {'form': form})


def signout(request):
    logout(request)
    return redirect("/signin/")
