from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoomForm
from .models import Room
# Create your views here.

def index(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        room_model = form.save()
        return redirect('chat:user', room_model.pk)
    queryset = Room.objects.order_by('-id')
    context = { 'form': form, 'queryset': queryset }
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    username = request.GET.get('username', 'Anonymus')
    return render(request, 'chat/chatroom.html', {'room_name': room_name, 'username':username})

def user(request,pk):
    room = Room.objects.get(pk=pk)
    return render(request, 'chat/room.html', {'room_name':room.room_name})
