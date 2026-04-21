from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from reviews.forms import ReviewForm
from reviews.models import Review
from reviews.utils import generate_slug
from users.models import UserRoles


class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    extra_context = {
        'title': 'Наши отзывы'
    }
    template_name = 'reviews/reviews.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=True)
        return queryset


class ReviewDeactivatedListView(LoginRequiredMixin, ListView):
    model = Review
    context_object_name = 'reviews'
    extra_context = {
        'title': 'Неактивные отзывы'
    }
    template_name = 'reviews/reviews.html'
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        # Администратор или модератор могут просматривать неактивные отзывы
        if request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            messages.warning(request, 'Доступ запрещен. Только для администраторов и модераторов.')
            return redirect('reviews:reviews_list')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sign_of_review=False).select_related('sight', 'author')
        return queryset


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    extra_context = {
        'title': 'Добавить отзыв'
    }
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Для добавления отзыва необходимо авторизоваться')
            return redirect('users:user_login')

        # Проверяем, что пользователь не админ и не модератор
        if request.user.role == UserRoles.ADMIN or request.user.role == UserRoles.MODERATOR:
            messages.error(request, 'Администраторы и модераторы не могут оставлять отзывы')
            return redirect('reviews:reviews_list')

        # Проверяем, что пользователь имеет роль USER
        if request.user.role != UserRoles.USER:
            messages.error(request, 'Только обычные пользователи могут оставлять отзывы')
            return redirect('reviews:reviews_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.role != UserRoles.USER:
            messages.error(self.request, 'Только обычные пользователи могут оставлять отзывы')
            return HttpResponseForbidden("Только обычные пользователи могут оставлять отзывы")

        review_object = form.save(commit=False)
        review_object.author = self.request.user

        # Генерируем slug, если его нет
        if not review_object.slug or review_object.slug == 'temp_slug':
            from reviews.utils import generate_slug
            review_object.slug = generate_slug()

        review_object.save()
        messages.success(self.request, 'Отзыв успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании отзыва. Проверьте правильность заполнения.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('reviews:review_detail', kwargs={'slug': self.object.slug})


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/detail.html'
    context_object_name = 'review'
    extra_context = {
        'title': 'Просмотр отзыва'
    }


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/create_update.html'
    login_url = '/users/login/'

    def get_success_url(self):
        return reverse_lazy('reviews:review_detail', kwargs={'slug': self.kwargs.get('slug')})

    def dispatch(self, request, *args, **kwargs):
        review_object = self.get_object()
        # Только автор может редактировать
        if review_object.author != self.request.user:
            messages.warning(request, 'Вы можете редактировать только свои отзывы')
            return redirect('reviews:review_detail', slug=review_object.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        review_object = super().get_object(queryset)
        return review_object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data()
        review_object = self.get_object()
        context_data['title'] = f'Изменить отзыв: {review_object.sight.name}'
        return context_data


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'reviews/delete.html'
    extra_context = {
        'title': 'Удалить отзыв'
    }
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        review_object = self.get_object()
        # Автор или админ могут удалять
        if review_object.author != self.request.user and self.request.user.role != UserRoles.ADMIN:
            messages.warning(request, 'Вы можете удалять только свои отзывы')
            return redirect('reviews:review_detail', slug=review_object.slug)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        review_object = super().get_object(queryset)
        return review_object

    def get_success_url(self):
        return reverse_lazy('reviews:reviews_list')


@login_required
def review_toggle_activity(request, slug):
    review_object = get_object_or_404(Review, slug=slug)

    # Администратор или модератор могут изменять статус
    if request.user.role not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
        messages.error(request, 'Только администратор или модератор может изменять статус отзывов')
        raise PermissionDenied()

    if review_object.sign_of_review:
        review_object.sign_of_review = False
        review_object.save()
        messages.success(request, f'Отзыв "{review_object.title}" деактивирован')
        return redirect('reviews:reviews_deactivated')
    else:
        review_object.sign_of_review = True
        review_object.save()
        messages.success(request, f'Отзыв "{review_object.title}" активирован')
        return redirect('reviews:reviews_list')