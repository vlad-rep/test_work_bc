from django.contrib.auth.views import LoginView
from django.contrib.auth import models
from django.db.models import Q
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render
from django.views import generic

from chat.forms import UserCreateForm
from chat.models import User, Message


class UserCreateView(generic.CreateView):
    model = User
    template_name = 'chat/registration.html'
    form_class = UserCreateForm
    success_url = '/'

    def check(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            error_message = 'Этот логин уже занят'
            return error_message


class AnotherLoginView(LoginView):
    template_name = 'chat/login.html'


class FindUser(ListView):
    model = User, Message
    template_name = 'chat/find_user.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = User.objects.filter(
            Q(username=query))

        if object_list:
            receiver_id = object_list[0].id
            self.request.session['receiver_id'] = receiver_id
            receiver_name = object_list[0].username
            self.request.session['receiver_name'] = receiver_name
        return object_list


class ChatRoom(View):

    def get(self, request):
        sender = request.user.id
        receiver = request.session.get('receiver_id')
        receiver_name = request.session.get('receiver_name')

        message_history = Message.objects.filter(
            Q(sender=sender) & Q(receiver=receiver)
        )
        message_history_reverse = Message.objects.filter(
            Q(sender=receiver) & Q(receiver=sender)
        )

        new_message = self.request.GET.get('new_massage')
        if new_message:
            new_message_to_db = Message(text=new_message,
                                        sender=User.objects.get(pk=sender),
                                        receiver=User.objects.get(pk=receiver))
            new_message_to_db.save()
        else:
            pass

        return render(request, 'chat/chat_room.html',
                      {'message_history': message_history, 'message_history_reverse': message_history_reverse,
                       'receiver_name': receiver_name,
                       'receiver': receiver, 'sender': sender})
