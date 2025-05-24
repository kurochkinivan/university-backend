from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=150, label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class RegisterForm(forms.Form):
    login = forms.CharField(max_length=150, label="Логин")
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")
