from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from sights.forms import SightForm, CategoryForm
from sights.models import Sight, Category


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Мурманск - Главная',
    }
    return render(request, 'sights/index.html', context)


class SightsListView(ListView):
    model = Sight
    extra_context = {
        'title': 'Питомник все наши собаки'
    }

    template_name = 'sights/sights.html'

class SightsDetailView(DetailView):
    model = Sight
    template_name = 'sights/sights_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        sight_object = self.get_object()
        context_data['title'] = f'Подробная информация\n{sight_object}'
        return context_data

# @login_required(login_url='users:user_login')
# def sight_detail(request, pk: int):
#     sight = get_object_or_404(Sight, pk=pk)
#     context = {
#         'sight': sight,
#         'title': sight.name,
#     }
#     return render(request, 'sights/sights_detail.html', context)


class SightsCreateView(CreateView):
    model = Sight
    form_class = SightForm
    template_name = 'sights/sights_update_create.html'
    extra_context = {
        'title': 'Добавить достопримечательность'
    }
    success_url = reverse_lazy('sights:index')


@login_required(login_url='users:user_login')
def sights_update_view(request, pk):
    sight_object = get_object_or_404(Sight, pk=pk)
    if request.method == 'POST':
        form = SightForm(request.POST, request.FILES, instance=sight_object)
        if form.is_valid():
            sight_object = form.save()
            sight_object.save()
            return HttpResponseRedirect(reverse('sights:sight_detail', args=(pk,)))
    context = {
        'title': 'Изменить достопримечательность',
        'object': sight_object,
        'form': SightForm(instance=sight_object)
    }
    return render(request, 'sights/sights_update_create.html', context)


@login_required(login_url='users:user_login')
def sights_delete_view(request, pk):
    sight_object = get_object_or_404(Sight, pk=pk)
    if request.method == 'POST':
        sight_object.delete()
        return HttpResponseRedirect(reverse('sights:sight_list'))
    context = {
        'title': 'Удалить достопримечательность',
        'object': sight_object,
    }
    return render(request, 'sights/sights_delete.html', context)


def category_list(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Категории',
    }
    return render(request, 'sights/category_list.html', context)


@login_required(login_url='users:user_login')
def category_create_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sights:index'))
    context = {
        'title': 'Добавить категорию',
        'form': CategoryForm()
    }
    return render(request, 'sights/category_create.html', context)


def category_detail(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    sights = Sight.objects.filter(category=category)

    context = {
        'category': category,
        'sights': sights,
        'title': category.name,
    }
    return render(request, 'sights/category_detail.html', context)
