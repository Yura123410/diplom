from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.contrib import messages
from django.db.models import Q

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

    paginate_by = 6


class SightsDetailView(DetailView):
    model = Sight
    template_name = 'sights/sights_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка на модератора/админа
        is_moderator = (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))

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


class CategoryListView(ListView):
    model = Category
    context_object_name = 'object_list'
    extra_context = {'title': 'Категории'}
    template_name = 'sights/category_list.html'

    paginate_by = 3


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    login_url = 'users:user_login'
    success_url = reverse_lazy('sights:index')
    template_name = 'sights/category_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить категорию'
        return context


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    template_name = 'sights/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sights'] = Sight.objects.filter(category=self.object)
        context['title'] = self.object.name
        return context


# Работа с галереей
class AddPhotoView(LoginRequiredMixin, View):
    login_url = 'users:user_login'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return redirect('sights:sight_detail', pk=kwargs['pk'])

    def post(self, request, pk):
        sight = get_object_or_404(Sight, pk=pk)

        photo = request.FILES.get('photo')
        if photo:
            SightPhoto.objects.create(sight=sight, image=photo)
            messages.success(request, 'Фото добавлено!')

        return redirect('sights:sight_detail', pk=pk)


class DeletePhotoView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SightPhoto
    login_url = 'users:user_login'

    def test_func(self):
        # Только staff могут удалять фото
        return self.request.user.is_staff

    def get_success_url(self):
        # После удаления возвращаемся на страницу достопримечательности
        return reverse_lazy('sights:sight_detail', kwargs={'pk': self.object.sight.pk})

    def delete(self, request, *args, **kwargs):
        # Получаем объект до удаления
        self.object = self.get_object()
        sight_pk = self.object.sight.pk

        # Удаляем
        self.object.delete()
        messages.success(request, 'Фото удалено!')

        # Перенаправляем
        return redirect('sights:sight_detail', pk=sight_pk)

    def get(self, request, *args, **kwargs):
        # Блокируем GET-запросы (удаление только через POST)
        return redirect('sights:sight_detail', pk=self.get_object().sight.pk)


class AllSearchListView(ListView):
    model = Sight
    template_name = 'sights/all_search_results.html'

    extra_context = {
        'title': 'Результаты поискового запроса'
    }

    def get_queryset(self):
        query = self.request.GET.get('q')
        sight_object_list = Sight.objects.filter(
            Q(name__icontains=query)
        )
        category_object_list = Category.objects.filter(
            Q(name__icontains=query)
        )
        object_list = list(sight_object_list) + list(category_object_list)
        return object_list
