"""
Таблицы БД messenger
"""
import typing
from django.db import models
from django.contrib.auth.models import User


class GroupChat(models.Model):
    """
    Таблица групповых чатов
    """
    title: typing.Type[models.CharField] = models.CharField(
        max_length=255
    )

    def __str__(self) -> str:
        """
        Отображения названия группового чата
        """
        return str(self.title)


class Messages(models.Model):
    """
    Таблица с историей индивидуальных сообщений
    """
    message: typing.Type[models.CharField] = models.CharField(
        max_length=255
    )
    author: typing.Type[models.ForeignKey] = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_author'
    )
    created: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True
    )
    modified: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now=True
    )
    group_chat: typing.Type[models.ForeignKey] = models.ForeignKey(
        GroupChat, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """
        Отображения текста сообщения
        """
        return str(self.message)
