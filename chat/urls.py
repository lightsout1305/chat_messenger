from django.urls import path
from . import views


urlpatterns = [
    path('messages/', views.MessagesView.as_view()),
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    path('groupchats/', views.GroupChatView.as_view()),
]
