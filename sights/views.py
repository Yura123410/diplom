import json
import urllib.request
import re
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.db.models import Q
from django.forms import inlineformset_factory

from sights.forms import SightForm, CategoryForm, SightPhotoForm
from sights.models import Sight, Category, SightPhoto


def index(request):
    context = {
        'object_list': Category.objects.all()[:3],
        'title': 'Мурманск - Главная',
    }
    return render(request, 'sights/index.html', context)


def update_sight_coordinates(sight_instance):
    """
    Получает координаты (широту и долготу) для адреса 'sight.address'
    через API Яндекс.Геокодера и сохраняет их в экземпляр 'sight_instance'.
    """
    if not sight_instance.address:
        return False

    # Очищаем адрес от управляющих символов
    clean_address = sight_instance.address.strip()
    clean_address = re.sub(r'[\n\r\t\x0b\x0c]', ' ', clean_address)
    clean_address = re.sub(r'\s+', ' ', clean_address)

    # Кодируем адрес для безопасной передачи в URL
    from urllib.parse import quote
    encoded_address = quote(clean_address, safe='/:,.')

    # Формируем URL для запроса к API Яндекс.Геокодера
    geocode_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={settings.YANDEX_GEOCODER_API_KEY}&geocode={encoded_address}&format=json"

    try:
        with urllib.request.urlopen(geocode_url) as response:
            data = json.loads(response.read().decode('utf-8'))

        # Извлекаем координаты из ответа API
        coordinates_str = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        longitude, latitude = coordinates_str.split(' ')

        # Сохраняем координаты в модель
        sight_instance.latitude = float(latitude)
        sight_instance.longitude = float(longitude)
        sight_instance.save(update_fields=['latitude', 'longitude'])

        return True
    except Exception as e:
        print(f"Ошибка геокодирования для '{sight_instance.name}': {e}")
        return False


# Определяем FormSet для фотографий (на уровне модуля)
SightPhotoFormSet = inlineformset_factory(
    Sight,
    SightPhoto,
    form=SightPhotoForm,
    fields=('image',),
    extra=1,
    can_delete=True,
    can_order=True,
)


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

        is_moderator = (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))

        if not is_moderator:
            self.object.increment_views()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Подробная информация\n{self.object}'
        context_data['gallery_photos'] = self.object.photos.all()
        context_data['yandex_map_api_key'] = getattr(settings, 'YANDEX_GEOCODER_API_KEY', '')
        return context_data


class SightsCreateView(LoginRequiredMixin, CreateView):
    model = Sight
    form_class = SightForm
    template_name = 'sights/sights_update_create.html'
    extra_context = {
        'title': 'Добавить достопримечательность'
    }
    success_url = reverse_lazy('sights:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['photo_formset'] = SightPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['photo_formset'] = SightPhotoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']

        if photo_formset.is_valid():
            response = super().form_valid(form)
            photo_formset.instance = self.object
            photo_formset.save()

            if update_sight_coordinates(self.object):
                messages.success(self.request, f'Координаты для "{self.object.name}" успешно определены.')
            else:
                messages.warning(self.request, f'Не удалось определить координаты для адреса: "{self.object.address}".')

            return response
        else:
            return self.form_invalid(form)


class SightsUpdateView(LoginRequiredMixin, UpdateView):
    model = Sight
    form_class = SightForm
    template_name = 'sights/sights_update_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['photo_formset'] = SightPhotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['photo_formset'] = SightPhotoFormSet(instance=self.object)
        return context

    def get_object(self, queryset=None):
        sight_object = super().get_object(queryset)
        if self.request.user and not self.request.user.is_staff:
            raise Http404
        return sight_object

    def get_success_url(self):
        return reverse('sights:sight_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']

        if photo_formset.is_valid():
            response = super().form_valid(form)
            photo_formset.instance = self.object
            photo_formset.save()

            if update_sight_coordinates(self.object):
                messages.success(self.request, f'Координаты для "{self.object.name}" успешно обновлены.')
            else:
                messages.warning(self.request, f'Не удалось определить координаты для адреса: "{self.object.address}".')

            return response
        else:
            return self.form_invalid(form)


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


class AddPhotoView(LoginRequiredMixin, View):
    login_url = 'users:user_login'

    def post(self, request, pk):
        sight = get_object_or_404(Sight, pk=pk)
        photo = request.FILES.get('photo')

        if photo:
            if not photo.content_type.startswith('image/'):
                messages.error(request, 'Пожалуйста, загружайте только изображения')
            elif photo.size > 5 * 1024 * 1024:
                messages.error(request, 'Размер файла не должен превышать 5MB')
            else:
                SightPhoto.objects.create(sight=sight, image=photo)
                messages.success(request, 'Фото добавлено!')
        else:
            messages.error(request, 'Пожалуйста, выберите файл для загрузки')

        return redirect('sights:sight_detail', pk=pk)


class DeletePhotoView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = SightPhoto
    login_url = 'users:user_login'

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        sight_pk = self.object.sight.pk
        self.object.delete()
        messages.success(request, 'Фото удалено!')
        return redirect('sights:sight_detail', pk=sight_pk)

    def get(self, request, *args, **kwargs):
        return redirect('sights:sight_detail', pk=self.get_object().sight.pk)


class AllSearchListView(ListView):
    model = Sight
    template_name = 'sights/all_search_results.html'
    extra_context = {'title': 'Результаты поискового запроса'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        sight_object_list = Sight.objects.filter(Q(name__icontains=query))
        category_object_list = Category.objects.filter(Q(name__icontains=query))
        object_list = list(sight_object_list) + list(category_object_list)
        return object_list