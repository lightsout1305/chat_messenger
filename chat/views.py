from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import Messages, GroupChat
from .serializers import MessageSerializer, UserSerializer, GroupChatSerializer


class MessagesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    queryset = Messages.objects.all()

    def get_queryset(self):
        queryset = Messages.objects.all()
        group_chat = self.request.query_params.get('group-chat')
        if group_chat is not None:
            queryset = queryset.filter(group_chat=group_chat)
        return queryset

    def post(self, request, *args, **kwargs):
        serial = MessageSerializer(data=request.data)
        if serial.is_valid():
            message = Messages.objects.create(
                message=request.data['message'],
                author_id=request.user.id,
                group_chat_id=request.data['group_chat']
            )
            message.save()
            return Response(serial.data, status=status.HTTP_200_OK)
        else:
            return Response(serial.data, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.username = request.data.get('username')
        instance.first_name = request.data.get('first_name')
        instance.last_name = request.data.get('last_name')
        instance.save()

        serial = UserSerializer(data=request.data)
        if serial.is_valid(raise_exception=True):
            self.perform_update(serializer=serial)
            return Response(serial.data, status=status.HTTP_200_OK)
        else:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupChatView(generics.ListCreateAPIView):
    queryset = GroupChat.objects.all()
    serializer_class = GroupChatSerializer
    permission_classes = [IsAuthenticated]
