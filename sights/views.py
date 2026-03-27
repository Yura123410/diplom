from django.shortcuts import render

from sights.models import Sight, Category


def index(request):
    context = {
        'objects_list': Sight.objects.all()[:3],
        'title': 'Главная - Достопримечательности Мурманска',
    }
    return render(request, 'sights/index.html', context)
