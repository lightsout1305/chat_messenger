"""
Модуль сериализации моделей для DRF
"""
import typing
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.db.models import Model
from .models import GroupMessages, UserImage, GroupChat, Messages


class MessageSerializer(ModelSerializer):
    """
    Сериализация модели Messages
    """

    class Meta:
        """
        Настройка классовых переменных MessageSerializer
        """
        model: typing.ClassVar[Model] = Messages
        exclude = ('deleted',)


class GroupMessageSerializer(ModelSerializer):
    """
    Сериализация модели GroupMessages
    """

    class Meta:
        """
        Настройка классовых переменных GroupMessageSerializer
        """
        model: typing.ClassVar[Model] = GroupMessages
        exclude: typing.ClassVar[tuple] = ('deleted',)


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
            'first_name',
            'last_name',
            'username'
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
        exclude: typing.ClassVar[tuple] = ('deleted', )


class GroupChatSerializer(ModelSerializer):
    """
    Сериализация модели GroupChat
    """
    class Meta:
        """
        Настройка классовых переменных GroupChatSerializer
        """
        model: typing.ClassVar[Model] = GroupChat
        exclude = ('deleted',)
