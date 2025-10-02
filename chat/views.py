from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room 
from users.models import Profile


# Create your views here.
@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)
    users = Profile.objects.all()
    context = {
        "id": room.id,
        "host": room.host,
        "users": users,
    }
    return  render(request, "chat/room.html", context)