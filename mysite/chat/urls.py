from django.urls import path

from . import views


urlpatterns = [

    path('registration/', views.UserCreateView.as_view(), name='registration'),
    path('', views.FindUser.as_view(), name='find_user'),
    path('registration/sing_up/', views.AnotherLoginView.as_view(), name='another_login'),
    path('chat_room/', views.ChatRoom.as_view(), name='chat_room'),
]
