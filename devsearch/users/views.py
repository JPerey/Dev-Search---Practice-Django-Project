from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def profiles(requests):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}

    return render(requests, 'users/profiles.html', context)


def userProfile(requests, pk):
    profileObj = Profile.objects.get(id=pk)
    context = {
        'profile': profileObj,
    }

    return render(requests, 'users/user-profile.html', context)


def loginUser(requests):

    if requests.user.is_authenticated:
        return redirect('profiles')

    if requests.method == "POST":
        username = requests.POST["username"]
        password = requests.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            print("username does not exist")

        user = authenticate(requests, username=username, password=password)

        if user is not None:
            # <-- login function creates a session on the database for the user
            login(requests, user)
            return redirect('profiles')
        else:
            print('Username OR password is incorrect')

    context = {

    }
    return render(requests, 'users/login_register.html', context)


def logoutUser(requests):
    logout(requests)
    return redirect('login')
