from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Address, NGO, Event, Restraunts
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.utils import timezone
import requests
from django.contrib.auth import authenticate, login as login_User, logout as logout_User
from django.contrib.auth.decorators import login_required
# Create your views here.

class AddressView(CreateView):
    model = Address
    fields = ['address']
    template_name = 'addresses/home.html'
    success_url = '/home'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['access_token'] = 'pk.eyJ1IjoiazdrYXVzaGFsIiwiYSI6ImNsaDRqZXh4NDBsc3IzaG81NnIwdHpvNGcifQ.Zkv2dg9ykTIQQlkyeyg_HQ'
        context['addresses'] = Address.objects.all()
        context['NGOS'] = NGO.objects.all()
        context['Events'] = Event.objects.all()
        context['Restraunts'] = Restraunts.objects.all()
        context['time'] =  timezone.now().date()
        return context

def register(request):
    if request.method == 'POST':

        err_lst = []
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        hashed_password = make_password(password1)
        # users = User.objects.all()
        if len(password1)<9:
            messages.error(request, f'Password must be atleast 8 characters long!')
            err_lst.append("Check Password length")
        if(password1 != password2):
            messages.error(request, f'Passwords not Matching!')
            err_lst.append("Passwords not Matching!")
            print("Got data1")
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Account with this Username already exist.')
            err_lst.append("Account with this Username already exist.")
            print("Got data2")
        if User.objects.filter(email=email).exists():
            messages.error(request, f'This Email is Already linked to an existing Account.')
            err_lst.append("This Email is Already linked to an existing Account.")
            print("Got data3")

        if len(err_lst) == 0:
            print("Got data4")
            u1 = User(username = username, email= email, password = hashed_password)
            u1.save()
            print("User created successfully")
            messages.success(request, f'Accound created!')
            return redirect ('home')
        else:
            return render(request, 'addresses/register.html', {'err_lst': err_lst})

    else:
        return render (request, 'addresses/register.html')

    return render(request, 'myapp/register.html')   

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')    
        password = request.POST.get('password')
        users = User.objects.filter(username = username).first()
        if users is not None:
            username = users.username
            user =  authenticate(request, username=username, password=password)
            if user is not None:
                print("user is not none true")
                login_User(request, user)
                return redirect('home')
            else:
                print("error message wala")
                messages.success(request, f'Invalid Credentials!')
                return render(request, 'addresses/login.html')
        else:
            messages.success(request, f'Invalid Credentials!')
            return render(request, 'addresses/login.html')
    else:
        return render(request, 'addresses/login.html')

@login_required(login_url='/login/')
def logout(request):
    logout_User(request)
    messages.success(request, f'Logged out successfully!')
    return redirect(reverse("home"))

@login_required(login_url='/login/')
def addngo(request, format=None):
    if request.method == 'POST':
        ngo_name = request.POST.get('ngo_name')
        ngo_type = request.POST.get('ngo_type')
        location = request.POST.get('location')
        contact = request.POST.get('Contact')
        website = request.POST.get('website')
        social = request.POST.get('social')
        owner = request.user

        if NGO.objects.filter(ngo_name = ngo_name).exists():
            messages.error(request, f'A NGO with this title already exists!')
            return render (request, 'addresses/addngo.html')
        else:
            messages.success(request, f'NGO Live!')
            b1 = NGO(owner = owner, ngo_name=ngo_name, ngo_type=ngo_type, location = location, Contact = contact, website = website, social = social)
            b2 = Address(address = location)
            b2.save()
            b1.save()
            return redirect('home')
    return render(request, 'addresses/addngo.html')

@login_required(login_url='/login/')
def addevent(request, format=None):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_attendants = request.POST.get('event_attendants')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        # event_manager = request.POST.get('event_manager')
        owner = request.user

        if Event.objects.filter( event_name =  event_name).exists():
            messages.error(request, f'An Event with this title already exists!')
            return render (request, 'addresses/addevent.html')
        else:
            messages.success(request, f'Event Live!')
            b1 = Event(owner = owner,  event_name= event_name, event_attendants = event_attendants, location = location, Contact = contact)
            # b2 = Address(address = location)
            # b2.save()
            b1.save()
            return redirect('home')
    return render(request, 'addresses/addevent.html')

@login_required(login_url='/login/')
def addrestraunts(request, format=None):
    if request.method == 'POST':
        r_name = request.POST.get('r_name')
        average_food = request.POST.get('average_food')
        approx_people = int(average_food) * int(4)
        r_location = request.POST.get('r_location')
        r_contact = request.POST.get('r_contact')
        # event_manager = request.POST.get('event_manager')

        if Restraunts.objects.filter( r_name =  r_name).exists():
            messages.error(request, f'A Restraunt with this title already exists!')
            return render (request, 'addresses/addrestraunts.html')
        else:
            messages.success(request, f'Restraunt Live!')
            b1 = Restraunts(r_name= r_name, average_food = average_food, r_location = r_location, r_contact = r_contact, approx_people = approx_people)
            # b2 = Address(address = location)
            # b2.save()
            b1.save()
            return redirect('home')
    return render(request, 'addresses/addrestraunts.html')

@login_required(login_url='/login/')
def ngohome(request, format=None):
    context = {
        'NGOS' : NGO.objects.all(),
        'access_token' : 'pk.eyJ1IjoiazdrYXVzaGFsIiwiYSI6ImNsaDRqZXh4NDBsc3IzaG81NnIwdHpvNGcifQ.Zkv2dg9ykTIQQlkyeyg_HQ'
    }
    return render(request, 'addresses/ngohome.html', context)

@login_required(login_url='/login/')
def eventhome(request, format=None):
    # a = timezone.now
    # print(a - Event.objects.first().date_posted)
    context = {
        'time' : timezone.now,
        'user' : request.user,
        'Events' : Event.objects.all(),
        'My' : Event.objects.filter(owner = request.user),
        'MySize' : Event.objects.filter(owner = request.user).count,
        'access_token' : 'pk.eyJ1IjoiazdrYXVzaGFsIiwiYSI6ImNsaDRqZXh4NDBsc3IzaG81NnIwdHpvNGcifQ.Zkv2dg9ykTIQQlkyeyg_HQ'
    }
    return render(request, 'addresses/eventhome.html', context)

@login_required(login_url='/login/')
def deleteevent(request, ename=None, format=None):
    b1 =  Event.objects.get(event_name = ename)
    b1.delete()
    messages.info(request, f"Event deleted!")
    return redirect('eventhome')


