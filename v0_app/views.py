from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import RegisterForm, RecipeForm
from .models import Recipe


def about(request):
    context = {
        'title': 'Главная',

    }
    return render(request, 'v0_app/about.html', context)


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


def main_page(request):
    user = request.user
    results_qty = 3
    latest_recipes = Recipe.objects.order_by('-created_at')[:results_qty]
    context = {
        'title': 'Главная',
        'username': user.username,
        'latest_recipes': latest_recipes,
    }
    return render(request, 'v0_app/main_page.html', context)

@login_required
def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, f'Рецепт {recipe.id} добавлен')
            return redirect('recipe_add')
    else:
        form = RecipeForm()

    context = {
        'title': 'Добавить рецепт',
        'form': form,
    }

    return render(request, 'v0_app/recipe_add.html', context)

def recipe_show(request, pk):
    recipe_find = Recipe.objects.filter(id=pk).first()
    if recipe_find is None:
        messages.error(request, 'Рецепт не найден')
        return render(request, 'v0_app/blank.html')
    else:
        ingredients_list = recipe_find.ingredients.split('\n')
        cook_steps_list = recipe_find.cook_steps.split('\n')
        context = {
            'recipe': recipe_find,
            'ingredients_list': ingredients_list,
            'cook_steps_list': cook_steps_list,
        }
        return render(request, 'v0_app/recipe_show.html', context)

