from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib import messages

from sights.forms import SightForm, CategoryForm
from sights.models import Sight, Category, SightPhoto


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Мурманск - Главная',
    }
    return render(request, 'sights/index.html', context)


class SightsListView(ListView):
    model = Sight
    extra_context = {
        'title': 'Все достопримечательности'
    }
    template_name = 'sights/sights.html'


class SightsDetailView(DetailView):
    model = Sight
    template_name = 'sights/sights_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка на модератора/админа
        is_moderator = (request.user.is_authenticated and
                        (request.user.is_staff or request.user.is_superuser))

        # Увеличиваем просмотр только для обычных пользователей
        if not is_moderator:
            self.object.increment_views()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Подробная информация\n{self.object}'
        context_data['gallery_photos'] = self.object.photos.all()
        return context_data


class SightsCreateView(LoginRequiredMixin, CreateView):
    model = Sight
    form_class = SightForm
    template_name = 'sights/sights_update_create.html'
    extra_context = {
        'title': 'Добавить достопримечательность'
    }
    success_url = reverse_lazy('sights:index')


class SightsUpdateView(LoginRequiredMixin, UpdateView):
    model = Sight
    template_name = 'sights/sights_update_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        sight_object = self.get_object()
        context_data['title'] = f'Изменить\n{sight_object}'
        return context_data

    def get_object(self, queryset=None):
        sight_object = super().get_object(queryset)
        if self.request.user and not self.request.user.is_staff:
            raise Http404
        return sight_object

    def get_success_url(self):
        return reverse('sights:sight_detail', args=[self.kwargs.get('pk')])


class SightsDeleteView(LoginRequiredMixin, DeleteView):
    model = Sight
    template_name = 'sights/sights_delete.html'
    success_url = reverse_lazy('sights:sight_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        sight_object = self.get_object()
        context_data['title'] = f'Удалить\n{sight_object}'
        return context_data


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


# Работа с галереей
@login_required
def add_photo(request, pk):
    sight = get_object_or_404(Sight, pk=pk)

    if request.method == 'POST' and request.FILES.get('photo'):
        SightPhoto.objects.create(
            sight=sight,
            image=request.FILES['photo']
        )
        messages.success(request, 'Фото добавлено!')

    return redirect('sights:sight_detail', pk=pk)


@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(SightPhoto, pk=pk)
    sight_pk = photo.sight.pk

    if request.user.is_staff:
        photo.delete()
        messages.success(request, 'Фото удалено!')

    return redirect('sights:sight_detail', pk=sight_pk)
