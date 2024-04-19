from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import RegisterForm


def main_page(request):
    context = {'title': 'Главная'}
    return render(request, 'v0_app/blank.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'Логин или пароль неверны')
            return render(request, 'v0_app/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'v0_app/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login_ = form.cleaned_data.get('login_')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            if not User.objects.filter(username=login_).exists():
                print(f'записываем в базу {login_} {password} {email}')
                user = User.objects.create_user(username=login_, email=email, password=password
                                                )
            else:
                messages.error(request, 'Пользователь с таким email уже существует. Выберите другой')
                return render(request, 'v0_app/register.html', {'form': form})

            messages.success(request, 'Регистрация завершена успешно')
            return redirect('login')

        else:
            error_text = form.errors['__all__']
            messages.error(request, error_text)
            return render(request, 'v0_app/register.html', {'form': form})

    else:
        form = RegisterForm()
    return render(request, 'v0_app/register.html', {'form': form})
