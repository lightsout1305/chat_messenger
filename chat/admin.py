"""
Модуль настройки страницы администрирования
"""
from django.contrib import admin
from .models import GroupMessages, GroupChat, Messages


@admin.register(GroupMessages)
class GroupMessagesAdmin(admin.ModelAdmin):
    """
    Регистрация модели GroupMessages на странице администрирования
    """
    list_display: list = ['message', 'created', 'author', 'group_chat']
    list_filter: list = ['author', 'group_chat', 'created']


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    """
    Регистрации модели GroupChat на странице администрирования
    """
    list_display: list = ['title']


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    """
    Регистрация модели Messages на странице администрирования
    """
    list_display: list = ['message', 'created', 'author', 'recipient']
    list_filter = ['author', 'recipient', 'created']
