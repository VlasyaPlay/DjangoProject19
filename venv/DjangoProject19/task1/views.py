from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .forms import UserRegister
from .models import Buyer, Game

# Create your views here.
def platform(request):
    title = 'platform'
    text = 'Главная страница'
    context = {
        'title': title,
        'text': text,
    }
    return render(request, 'platform.html', context)


def shop(request):
    title = 'games'
    text = 'Игры'
    games = Game.objects.all()

    context = {
        'title': title,
        'text': text,
        'games': games,
    }
    return render(request, 'games.html', context)


def cart(request):
    title = 'cart'
    text = 'Корзина'
    content = 'Извините, покупка игр временно недоступна'
    context = {
        'title': title,
        'content': content,
        'text': text,
    }
    return render(request, 'cart.html', context)

def sing_app_by_django(request):
    info = {}

    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            try:
                age = int(age)
            except (TypeError, ValueError):
                age = 0

            if password != repeat_password:
                info['error'] = 'Пароли не совпалают'
            elif age < 18:
                info['error'] = 'Вы должны быть старше 18 лет'
            else:
                if Buyer.objects.filter(name=username).exists():
                    info['error'] = 'Пользователь уже существует'
                else:
                    Buyer.objects.create(name=username, password=password, age=age)
                    return HttpResponse(f'Приветствуем, {username}')
        info['form'] = form
    else:
        form = UserRegister()
        info['form'] = form

    return render(request, 'registration_page.html', info)


def sign_up_by_html(request):
    info = {}

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        age = request.POST.get('age')

        try:
            age = int(age)
        except (TypeError, ValueError):
            age = 0

        if password != repeat_password:
            info['error'] = 'Пароли не совпалают'
        elif age < 18:
            info['error'] = 'Вы должны быть старше 18 лет'
        else:
            if Buyer.objects.filter(name=username).exists():
                info['error'] = 'Пользователь уже существует'
            else:
                Buyer.objects.create(name=username, password=password, age=age)
                return HttpResponse(f'Приветствуем, {username}')

    return render(request, 'registration_page.html', info)