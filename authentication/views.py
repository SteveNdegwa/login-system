from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from .forms import SigninForm, SignupForm, ForgotPasswordForm, ChangePasswordForm
from random import randint


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
    # else:
    form = SignupForm()
    return render(request, 'authentication/signup.html', {'form': form})


def signout(request):
    logout(request)
    return redirect("/signin/")


def forgot_password(request):
    if request.method == 'GET':
        form = ForgotPasswordForm()
        return render(request, 'authentication/forgot_password.html', {'form': form})
    else:
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                return redirect(f"/change-password/{email}")
            else:
                form = ForgotPasswordForm()
                return render(request, 'authentication/forgot_password.html', {'form': form, 'error': "Email doesn't exist in the database"})
        else:
            form = ForgotPasswordForm()
            return render(request, 'authentication/forgot_password.html', {'form': form, 'error': "Invalid Email"})


def change_password(request, email):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            new_password2 = form.cleaned_data['new_password2']
            otp = form.cleaned_data['otp']
            if otp != str(request.session['otp']):
                return render(request, 'authentication/change_password.html',{'form': form, 'email':email, 'error': 'Invalid OTP'})
            else:
                if new_password != new_password2:
                    return render(request, 'authentication/change_password.html',{'form': form, 'email':email, 'error': "Passwords don't match"})
                else:
                    del request.session['otp']
                    user = User.objects.get(email=email)
                    user.password = new_password
                    user.save()
                    return redirect("/signin/")
        # else:
        return render(request, 'authentication/change_password.html', {'form': form, 'email':email, 'error':'Invalid details'})

    # GET
    else:
        otp = randint(1000, 9999)
        print(otp)
        request.session['otp'] = otp
        # send_mail(
        #     "OTP",
        #     f"Your OTP is: {otp}",
        #     "stevencallistus19@gmail.com",
        #     [email],
        #     fail_silently=False,
        # )
        form = ChangePasswordForm()
        return render(request, 'authentication/change_password.html', {'form': form, 'email': email})



