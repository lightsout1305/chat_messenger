"""
Модуль с настроенными правами доступа
"""
from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model


class IsProfileOwner(BasePermission):
    """
    Права доступа владельца профиля
    """
    def has_permission(self, request, view) -> bool:
        """
        Проверка, авторизован ли пользователь
        """

        if request.user.is_authenticated or request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        owner = get_user_model().objects.get(id=obj.id)
        if owner == request.user or request.user.is_staff:
            return True
        return False

