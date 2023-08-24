from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Tweet, Follower


def home(request):
    tweets = Tweet.objects.all()
    context = {'tweets': tweets}

    if request.method == 'POST':
        tweet = Tweet()
        tweet.user = request.user
        tweet.tweet = request.POST.get('tweet')
        tweet.save()
        return redirect('home')

    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password invalid.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def profile(request):
    if request.user.is_authenticated: 
        tweets = Tweet.objects.filter(user = request.user)
        
        fullName = User.get_full_name(request.user)
        context = {'user': request.user, 'fullName': fullName, 'tweets': tweets}

        return render(request, 'base/profile.html', context)
    
    redirect('home')

def editProfile(request):    
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()            
        
        context = {'user': request.user}
        return render(request, 'base/editProfile.html', context)
    
    redirect('home')

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    tweets = Tweet.objects.filter(user = user)
    fullName = User.get_full_name(user)
    
    context = {'user': user, 'fullName': fullName, 'tweets': tweets}

    return render(request, 'base/profile.html', context)
    
    redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()    
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')

    return render(request, 'base/login_register.html', {'form': form})

def follow(request, pk):
    follower = Follower()
    follower.user = User.objects.get(id=pk)
    follower.follower = request.user
    follower.save()
    
    return redirect('userProfile', pk=pk)
