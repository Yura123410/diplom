from django.shortcuts import render, get_object_or_404

from sights.models import Sight, Category


def index(request):
    context = {
        'objects_list': Sight.objects.all()[:3],
        'title': 'Главная - Достопримечательности Мурманска',
    }
    return render(request, 'sights/index.html', context)

def sight_list(request):
    context = {
        'objects_list': Sight.objects.all(),
        'title': 'Все достопримечательности',
    }
    return render(request, 'sights/sight_list.html', context)

def sight_detail(request, pk: int):
    sight = get_object_or_404(Sight, pk=pk)
    context = {
        'sight': sight,
        'title': sight.name,
    }
    return render(request, 'sights/sight_detail.html', context)