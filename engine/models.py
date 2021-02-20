from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    users = models.ManyToManyField(User)


class BaseMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MainChannelMessage(BaseMessage):
    pass


class TeamMessage(BaseMessage):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class PrivateMessage(BaseMessage):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
