"""
Таблицы БД messenger
"""
import typing
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class GroupChat(models.Model):
    """
    Таблица групповых чатов
    """
    title: typing.Type[models.CharField] = models.CharField(
        max_length=255
    )
    slug: typing.Type[models.SlugField] = models.SlugField(
        max_length=100
    )
    created: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True
    )
    modified: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now=True
    )
    deleted: typing.Type[models.DateTimeField] = models.DateTimeField(
        blank=True, null=True
    )

    def __str__(self) -> str:
        """
        Отображения названия группового чата
        """
        return str(self.title)


class GroupMessages(models.Model):
    """
    Таблица с историей групповых сообщений
    """
    message: typing.Type[models.CharField] = models.CharField(
        max_length=255
    )
    author: typing.Type[models.ForeignKey] = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='group_message_author'
    )
    created: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True
    )
    modified: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now=True
    )
    deleted: typing.Type[models.DateTimeField] = models.DateTimeField(
        blank=True, null=True
    )
    group_chat: typing.Type[models.ForeignKey] = models.ForeignKey(
        GroupChat, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """
        Отображения текста сообщения
        """
        return str(self.message)


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
    deleted: typing.Type[models.DateTimeField] = models.DateTimeField(
        blank=True, null=True
    )
    recipient: typing.Type[models.ForeignKey] = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='message_recipient'
    )

    def __str__(self) -> str:
        """
        Отображения текста сообщения
        """
        return str(self.message)


class UserImage(models.Model):
    """
    Таблица с аватарами пользователей
    """
    user: typing.Type[models.ForeignKey] = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_photo'
    )
    image: typing.Type[models.ImageField] = models.ImageField()
    created: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now_add=True
    )
    modified: typing.Type[models.DateTimeField] = models.DateTimeField(
        auto_now=True
    )
    deleted: typing.Type[models.DateTimeField] = models.DateTimeField(
        blank=True, null=True
    )
