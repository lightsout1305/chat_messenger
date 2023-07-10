"""
Представления приложения chat
"""
from django.views.generic import ListView
from django.contrib.auth import get_user_model


class MainPageView(ListView):
    """
    Представление главной страницы со списком пользователей
    """
    template_name: str = 'chat/start_page.html'
    model: get_user_model = get_user_model()
    context_object_name: str = 'list_of_users'
