from django.http import HttpResponse
from django.shortcuts import render, redirect
from user_face.models import User
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect


# Create your views here.

def info(rec):
    return render(rec, 'register/info.html')


def con(rec):
    return render(rec, 'register/contact.html')


def logout(request):
    django_logout(request)
    return redirect('home')


def login(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        try:
            user = User.objects.get(login=login, password=password)

            # Сохраняем имя пользователя в сессии
            request.session['username'] = user.login
            # Выполняем перенаправление на домашнюю страницу

            return redirect('user', id=request.session['username'])

        except User.DoesNotExist:
            error_message = 'Неправильный логин или пароль.'
            return render(request, 'register/index.html', {'error_message': error_message})

    return render(request, 'register/index.html')


def home(request):
    return render(request, 'register/home.html')


def user(request, id):
    if id == 'admin':
        return render(request, 'user_face/user_admin.html')
    else:
        return render(request, 'user_face/user_user.html')
