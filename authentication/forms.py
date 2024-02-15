from django import forms


class SigninForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=7, required=True)


class SignupForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=7, required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, min_length=7, required=True)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True)


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=7, required=True)
    new_password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, min_length=7, required=True)
    otp = forms.CharField(min_length=4, max_length=4, required=True)
