from django.urls import path
from . import views


urlpatterns = [
    path('messages', views.GetMessages.as_view(), name='messages_list'),
    path('messages/create/', views.CreateMessage.as_view(), name='create_message'),
    path('groupmessages', views.GetGroupMessages.as_view(), name='group_messages_list'),
    path('groupmessages/create/', views.CreateGroupMessage.as_view(), name='create_groupmessage'),
    path('users/', views.GetUsers.as_view(), name='users_list'),
    path('users/<int:pk>/', views.GetUserInfo.as_view(), name='user_detail'),
    path('users/<int:pk>/update/', views.UpdateUserInfo.as_view(), name='update_user'),
    path('users/<int:user_id>/images/', views.GetUserImage.as_view(), name='user_image'),
    path('users/<int:user_id>/images/create/', views.CreateUserImage.as_view(), name='create_user_image'),
    path('users/<int:user_id>/images/update/', views.UpdateUserImage.as_view(), name='update_user_image'),
    path('groupchats/', views.GetGroupChat.as_view(), name='group_chat_list'),
    path('groupchats/<int:pk>/', views.GetGroupChatInfo.as_view(), name='group_chat_detail'),
    path('groupchats/create/', views.CreateGroupChat.as_view(), name='create_group_chat'),
    path('groupchats/<int:pk>/update/', views.UpdateGroupChat.as_view(), name='update_group_chat'),
    path('groupchats/<int:pk>/delete/', views.DeleteGroupChat.as_view(), name='delete_group_chat'),
]
