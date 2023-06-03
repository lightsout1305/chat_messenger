"""
Модуль настройки страницы администрирования
"""
from django.contrib import admin
from .models import Messages, GroupChat


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    """
    Регистрация модели Messages на странице администрирования
    """
    list_display: list = ['message', 'created', 'author', 'group_chat']


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    """
    Регистрации модели GroupChat на странице администрирования
    """
    list_display: list = ['title']
