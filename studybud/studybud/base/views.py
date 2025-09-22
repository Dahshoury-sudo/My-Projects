from django.shortcuts import render,redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Username Or Password Are Wrong')
            return redirect('login')
        
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Password Is Wrong')
    context = {'page':page}
    return render(request,'base/login_register.html',context)


def logoutuser(request):
    logout(request)
    return redirect('home')



def registerpage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # that False commit means "Create the object in memory, but do not save it to the database yet."
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An Error Occurred Please Try Again")
    context = {'page':page,'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains = q) |
        Q(description__contains = q)|
        Q(name__contains = q)
        )
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        room__topic__name__contains = q
    )
    topics = Topic.objects.all()[0:5]
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages} # pass rooms with alias 'rooms' to the home.html
    return render(request,"base/home.html",context)

def room(request,pk):
    room = Room.objects.get(id = pk)
    messages = room.message_set.all().order_by('-created') # Get all messages that are related to this room Note: message is a child of room
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)

    context = {"room":room,'room_messages':messages,'participants':participants}
    return render(request, 'base/room.html',context)

def userprofile(request,pk):
    user = User.objects.get(id=pk)
    # rooms = Room.objects.filter(host = user) this also works as 'rooms'
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def createroom(request):
    form = RoomForm() # make an empty form
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic_dumb, created = Topic.objects.get_or_create(name=topic_name)

        room = Room.objects.create(
            host = request.user,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            topic = topic_dumb,
        )
        room.participants.add(request.user)
        return redirect('home')
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room) #Creates a form pre-filled with existing data (for editing) , make a form with existing "room" data
    topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic').capitalize()
        room.name = request.POST.get('name')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        if topic != room.topic:
            room.topic.delete()
            room.topic = topic
        room.description = request.POST.get('description')
        
        room.save()
        return redirect ('home')

    context = {'form':form,'topics':topics,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteroom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect ('home')
    return render (request,'base/delete.html',{'obj':room})


@login_required(login_url='login')
def deletemessage(request,pk):
    message = Message.objects.get(id = pk)
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render (request,'base/delete.html',{'obj':message})


@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',user.id)
        
    context = {'form':form}
    return render(request,'base/update-user.html',context)


def topicspage(request): # For Mobile Responsiveness
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        name__contains = q,

    )
    context = {'topics':topics}
    return render(request,'base/topics.html',context)


def activitypage(request): # For Mobile Responsiveness
    room_messages = Message.objects.all()

    context = {'room_messages':room_messages}
    return render(request,'base/activity.html',context)