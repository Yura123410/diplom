from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from sights.forms import SightForm
from sights.models import Sight, Category


def index(request):
    context = {
        'objects': Category.objects.all()[:3],
        'title': 'Мурманск - Главная',
    }
    return render(request, 'sights/index.html', context)


def sight_list(request):
    context = {
        'objects_list': Sight.objects.all(),
        'title': 'Все достопримечательности',
    }
    return render(request, 'sights/sight_list.html', context)


def category_list(request):
    context = {
        'objects_list': Category.objects.all(),
        'title': 'Категории',
    }
    return render(request, 'sights/category_list.html', context)


def sight_detail(request, pk: int):
    sight = get_object_or_404(Sight, pk=pk)
    context = {
        'sight': sight,
        'title': sight.name,
    }
    return render(request, 'sights/sight_detail.html', context)


def sight_create_view(request):
    if request.method == 'POST':
        form = SightForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sight_list.html'))
    context = {
        'title': 'Добавить достопримечательность',
        'form': SightForm()
    }
    return render(request, 'sights/create.html', context)


def category_detail(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    sights = Sight.objects.filter(category=category)

    context = {
        'category': category,
        'sights': sights,
        'title': category.name,
    }
    return render(request, 'sights/category_detail.html', context)
