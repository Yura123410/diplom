from django.urls import path

from django.views.generic import TemplateView
from users.apps import UsersConfig
from users.views import UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, UserUpdateView, \
    UserPasswordChangeView, user_generate_new_password_view, UserListView, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    # Работа с аккаунтом
    path('', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change_password/', UserPasswordChangeView.as_view(), name='user_change_password'),
    path('profile/genpassword', user_generate_new_password_view, name='user_generate_password'),

    # Просмотр других пользователей
    path('all_users/', UserListView.as_view(), name='users_list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),

    # Страница пользовательского соглашения
    path('terms/', TemplateView.as_view(template_name='users/terms_of_service.html'), name='terms_of_service'),
]
