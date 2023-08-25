from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Tweet, Follower


def home(request, pk=''):
    tweets = None
    
    if pk == 'following':
        usersFollowed = Follower.objects.filter(follower = request.user)
        tweets = Tweet.objects.filter(user__followed__in=usersFollowed)
    else:
        tweets = Tweet.objects.all()

    context = {'tweets': tweets, 'filter': pk}

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

        followersCount = Follower.objects.filter(user = request.user).count
        followingCount = Follower.objects.filter(follower = request.user).count

        context = {'user': request.user, 'fullName': fullName, 'tweets': tweets, 
                   'followersCount': followersCount, 'followingCount': followingCount}

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

    followers = Follower.objects.filter(user = user)
    following = Follower.objects.filter(follower = user)
    
    followActive = followers.filter(follower = request.user)
    
    context = {'user': user, 'fullName': fullName, 'tweets': tweets, 'followActive': followActive,
               'followersCount': followers.count, 'followingCount': following.count}

    return render(request, 'base/profile.html', context)
    

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

def unfollow(request, pk):
    follower = Follower.objects.get(user = User(id=pk), follower = request.user)
    follower.delete()
    
    return redirect('userProfile', pk=pk)

def deleteTweet(request, pk, path):
    tweet = Tweet.objects.get(id=pk)

    if request.user == tweet.user:
        
        if request.method == 'POST':
            tweet.delete()
            next = request.POST.get('next', '/')
            return redirect(next)  
        
        context = {'tweet': tweet, 'path': path}
        return render(request, 'base/deleteTweet.html', context)
    
    return redirect('home')


def followers(request, pk):
    user = User.objects.get(id = pk)
    fullName = user.get_full_name()
    followers = Follower.objects.filter(user = user)

    context = {'user': user, 'fullName': fullName, 'usersToDisplay': followers}

    return render(request, 'base/followers.html', context)


def following(request, pk):
    user = User.objects.get(id = pk)
    fullName = user.get_full_name()
    following = Follower.objects.filter(follower = user)

    context = {'user': user, 'fullName': fullName, 'usersToDisplay': following}

    return render(request, 'base/following.html', context)