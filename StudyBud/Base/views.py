from pydoc_data.topics import topics
from django.shortcuts import render,redirect
from .models import Room,Topic,Message , User
from .forms import MyUserCreationForm, RoomForms,UserForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.
'''
rooms = [
    {'id':1 ,'name':"fronted developer"},
    { 'id':2 ,'name' : 'backend developer'},
    { 'id':3, 'name' : 'blockchain developers'},
]
'''
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated :
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username and password does not match')
    context = {'page':page}
    return render(request, 'Base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    #page = 'regsiter'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'an error ocured during registration')

    return render(request,'Base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains =q) |
        Q(description__icontains = q) |
        Q(name__icontains = q)
    )[0:8]

    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]

    context = {
        'rooms':rooms,
        'topics':topics,
        'rooms_count':room_count,
        'room_messages':room_messages,
        }

    return render(request , 'Base/index.html',context)

def room(request,pk):
    #room = None
    #for i in rooms:
    #    if i['id'] == int(pk):
    #        room = i
    #you can acess the context via line below
    room  = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    #updating the send message so it appers after clicking enter
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'Base/room.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all()
    context = {
        'user':user,
        'rooms':rooms,
        'topics':topics,
        'room_messages':room_messages,
        }
    return render(request,'Base/user_profile.html',context)

@login_required(login_url='loginPage')
def create_room(request):
    form = RoomForms()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForms(request.POST)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            
        )
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
        
    context = {'forms':form,'topics':topics,}
    return render(request,'Base/room_form.html',context)

@login_required(login_url='loginPage')
def updatedRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForms(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("you are not allowed here")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'forms':form,"topic":topics,'room':room}
    return render(request,'Base/room_form.html',context)

@login_required(login_url='loginPage')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    #topic = Topic.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
     #   topic.delete()
        return redirect('home')
    return render(request,'Base/delete.html',{'obj':room})

@login_required(login_url='loginPage')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'Base/delete.html',{'message':message})

@login_required(login_url='loginPage')
def updateUser(request):
    user = request.user
    conetxt = {'form' :UserForm(instance=user)}

    if request.method == 'POST':
        form = UserForm(request.POST ,request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile',pk=user.id)

    return render(request,'Base/update-user.html',conetxt)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request,"Base/topics.html",{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()[0:5]
    return render(request,"Base/activity.html",{"room_messages":room_messages})