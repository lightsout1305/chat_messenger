"""
Модуль с API и представлениями проекта
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.response import Response

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
            queryset = queryset.filter(recipient__username=recipient,
                                       deleted=None).order_by('created')
        elif author is not None and recipient is None:
            queryset = queryset.filter(author__username=author,
                                       deleted=None).order_by('created')
        elif author is not None and recipient is not None:
            queryset = queryset.filter(author__username=author,
                                       recipient__username=recipient).order_by('created')
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
            queryset = queryset.filter(group_chat__slug=group_chat, deleted=None).order_by('created')
        return queryset


class CreateGroupMessage(generics.CreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]


class GetUsers(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = get_user_model().objects.all().order_by('id')
        return queryset


class GetUserInfo(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class UpdateUserInfo(generics.UpdateAPIView):
    permission_classes = [IsProfileOwner]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class GetGroupChats(generics.ListAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = GroupChat.objects.filter(deleted=None).order_by('id')
        return queryset


class GetGroupChatInfo(generics.RetrieveAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        group_chat = GroupChat.objects.get(id=kwargs['pk'])
        pk = group_chat.pk
        title = group_chat.title
        slug = group_chat.slug
        group_chat_data = {
            "id": pk,
            "title": title,
            "slug": slug
        }
        if group_chat.deleted is None:
            return Response(group_chat_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateGroupChat(generics.CreateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]


class UpdateGroupChat(generics.UpdateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]
    queryset = GroupChat.objects.all()


class DeleteGroupChat(generics.CreateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]
    queryset = GroupChat.objects.all()

    def post(self, request, *args, **kwargs):
        post = GroupChat.objects.get(id=kwargs["pk"])
        if not post.deleted:
            post.deleted = timezone.now()
            post.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserImage(generics.CreateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsProfileOwner]
    lookup_field = 'user_id'

    def post(self, request, *args, **kwargs):
        user_image = UserImage.objects.filter(user_id=kwargs['user_id'], deleted=None).last()
        if not user_image:
            user_image = UserImage.objects.create(user_id=kwargs['user_id'], image=request.data['image'])
            user_image.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUserImage(generics.RetrieveAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserImage.objects.all()
    lookup_field = 'user_id'

    def get(self, request, *args, **kwargs):
        user_image = UserImage.objects.filter(user_id=kwargs['user_id'], deleted=None).last()
        if not user_image:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            data = self.serializer_class(user_image)
            return Response(data=data.data, status=status.HTTP_200_OK)


class UpdateUserImage(generics.UpdateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsProfileOwner]
    queryset = UserImage.objects.all()
    lookup_field = 'user_id'

    def put(self, request, *args, **kwargs):
        user_image = UserImage.objects.filter(user_id=kwargs["user_id"], deleted=None).last()
        if not user_image:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serial = self.serializer_class(None, request.data)
            if serial.is_valid():
                user_image.user = get_user_model().objects.get(id=kwargs['user_id'])
                user_image.image = request.data['image']
                user_image.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class DeleteUserImage(generics.CreateAPIView):
    serializer_class = UserImageSerializer
    permission_classes = [IsProfileOwner]
    queryset = UserImage.objects.all()
    lookup_field = 'user_id'

    def post(self, request, *args, **kwargs):
        user_image = UserImage.objects.filter(user_id=kwargs["user_id"], deleted=None).last()
        if not user_image:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_image.deleted = timezone.now()
            user_image.save()
            return Response(status=status.HTTP_200_OK)
