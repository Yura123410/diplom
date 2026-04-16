from django.contrib.auth import logout
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class CheckUserPermissionsMiddleware(MiddlewareMixin):
    """Middleware для проверки изменения прав пользователя"""

    def process_request(self, request):
        if request.user.is_authenticated:
            force_logout = cache.get(f'force_logout_{request.user.pk}')
            if force_logout:
                cache.delete(f'force_logout_{request.user.pk}')
                logout(request)
                from django.contrib import messages
                messages.warning(request, 'Ваши права были изменены. Пожалуйста, войдите снова.')