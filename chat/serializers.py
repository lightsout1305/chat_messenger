"""
Модуль сериализации моделей для DRF
"""
import typing
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.db.models import Model
from .models import Messages, UserImage, GroupChat


class MessageSerializer(ModelSerializer):
    """
    Сериализация модели Messages
    """

    class Meta:
        """
        Настройка классовых переменных MessageSerializer
        """
        model: typing.ClassVar[Model] = Messages
        fields: typing.ClassVar[tuple] = "__all__"


class UserSerializer(ModelSerializer):
    """
    Сериализация модели User
    """
    class Meta:
        """
        Настройка классовых переменных UserSerializer
        """
        model: typing.ClassVar[Model] = get_user_model()
        fields: typing.ClassVar[tuple] = (
            'id',
            'username',
            'first_name',
            'last_name'
        )


class UserImageSerializer(ModelSerializer):
    """
    Сериализация модели UserImage
    """
    class Meta:
        """
        Настройка классовых переменных UserImageSerializer
        """
        model: typing.ClassVar[Model] = UserImage
        fields: typing.ClassVar[tuple] = "__all__"


class GroupChatSerializer(ModelSerializer):
    """
    Сериализация модели GroupChat
    """
    class Meta:
        """
        Настройка классовых переменных GroupChatSerializer
        """
        model: typing.ClassVar[Model] = GroupChat
        fields: typing.ClassVar[tuple] = (
            'id',
            'title'
        )
