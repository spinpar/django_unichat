from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room 


# Create your views here.
@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)

    context = {
        "id": room.id,
        "host": room.host,
    }
    return  render(request, "chat/room.html", context)