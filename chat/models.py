from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    text = models.CharField(max_length=1500)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FK_message_user_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='FK_message_user_receiver')
    time = models.DateTimeField(auto_now=True)
