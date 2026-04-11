from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

from users.forms import UserRegisterForm, UserLoginForm


def user_register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('sights:index'))
    else:
        form = UserRegisterForm()  # создаём экземпляр формы для GET запроса

    context = {
        'title': 'Создать аккаунт',
        'form': form
    }
    return render(request, 'users/user_register.html', context=context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('sights:index'))
                return HttpResponse('Аккаунт неактивен')
            return HttpResponse('Нет такого пользователя!')
    context = {
        'title': 'Авторизация',
        'form': UserLoginForm
    }
    return render(request, 'users/user_login.html', context=context)


def user_profile_view(request):
    user_object = request.user
    context = {
        'title': f'Ваш профиль {user_object}'
    }
    return render(request, 'users/user_profile_read_only.html', context=context)
