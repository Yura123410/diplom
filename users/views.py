from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from users.forms import UserRegisterForm

def user_register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            print(form.cleaned_data['password'])
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect(reverse('sights:index'))
    else:
        form = UserRegisterForm() # создаём экземпляр формы для GET запроса

    context = {
        'title': 'Создать аккаунт',
        'form': form
    }
    return render(request, 'users/user_register.html', context=context)