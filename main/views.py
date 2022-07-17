from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, CustomUserCreationForm
from .decorators import unauthenticated_user
from .models import Room, Message


@login_required(login_url='login')
def home(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms,
    }
    return render(request, 'main/home.html', context)


@login_required(login_url='login')
def room(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_members = room.members.all()
    room_messages = room.message_set.all()
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            text=request.POST.get('message'),
        )
        room.members.add(request.user)
        return redirect('room', room.pk)

    context = {
        'room': room,
        'room_members': room_members,
        'room_messages': room_messages,
    }
    return render(request, 'main/room.html', context)


@login_required(login_url='login')
def room_create(request):
    form = RoomForm()
    next_page = request.GET.get('next') if request.GET.get('next') is not None else ''
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            room.host = request.user
            return redirect(next_page)

    context = {
        'form': form,
        'title': 'Create room',
    }
    return render(request, 'main/room_form.html', context)


def room_update(request, pk):
    room = get_object_or_404(Room, id=pk, host=request.user)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form,
        'title': 'Update room',
    }
    return render(request, 'main/room_form.html', context)


def room_delete(request, pk):
    room = get_object_or_404(Room, id=pk, host=request.user)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {
        'room': room,
    }
    return render(request, 'main/room_delete.html', context)


def message_delete(request, pk):
    message = get_object_or_404(Message, id=pk, user=request.user)
    message.delete()
    next_page = request.GET.get('next') if request.GET.get('next') is not None else ''
    return redirect(next_page)


@unauthenticated_user
def user_register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    context = {
        'form': form,
    }
    return render(request, 'main/accounts/register.html', context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'main/accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')
