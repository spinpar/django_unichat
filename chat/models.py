from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    #course

    def __str__(self):
        return self.name
    
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[0:50]
