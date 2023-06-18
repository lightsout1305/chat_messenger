"""
Модуль с API и представлениями проекта
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .models import GroupMessages, GroupChat, UserImage, Messages
from .serializers import GroupMessageSerializer, UserSerializer, GroupChatSerializer, \
    UserImageSerializer, MessageSerializer
from .permissions import IsProfileOwner


class GetMessages(generics.ListAPIView):
    """
    API получения списка сообщений пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Получить список сообщений с фильтрацией по id автора и id получателя
        """
        queryset = Messages.objects.all()
        recipient = self.request.query_params.get('recipient')
        author = self.request.query_params.get('author')
        if recipient is not None and author is None:
            queryset = queryset.filter(recipient__username=recipient)
        elif author is not None and recipient is None:
            queryset = queryset.filter(author__username=author)
        elif author is not None and recipient is not None:
            queryset = queryset.filter(author__username=author,
                                       recipient__username=recipient)
        return queryset


class CreateMessage(generics.CreateAPIView):
    """
    API создания сообщения
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer


class GetGroupMessages(generics.ListAPIView):
    """
    API получения сообщений группы с фильтрацией по id группового чата
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GroupMessageSerializer

    def get_queryset(self):
        queryset = GroupMessages.objects.all()
        group_chat = self.request.query_params.get('group-chat')
        if group_chat is not None:
            queryset = queryset.filter(group_chat__slug=group_chat)
        return queryset


class CreateGroupMessage(generics.CreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]


class GetUsers(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class GetUserInfo(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class UpdateUserInfo(generics.UpdateAPIView):
    permission_classes = [IsProfileOwner]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class GetGroupChat(generics.ListAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]


class GetGroupChatInfo(generics.RetrieveAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]


class CreateGroupChat(generics.CreateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]


class UpdateGroupChat(generics.UpdateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]
    queryset = GroupChat.objects.all()


class DeleteGroupChat(generics.DestroyAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]
    queryset = GroupChat.objects.all()


class CreateUserImage(generics.CreateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = 'user_id'


class GetUserImage(generics.RetrieveAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = UserImage.objects.all()
    lookup_field = 'user_id'


class UpdateUserImage(generics.UpdateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = UserImage.objects.all()
    lookup_field = 'user_id'
