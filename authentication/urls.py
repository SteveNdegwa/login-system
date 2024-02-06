from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('signout/', views.signout),
    path('forgot-password/', views.forgot_password),
    path('change-password/<str:email>/', views.change_password, name="change_password"),
]
