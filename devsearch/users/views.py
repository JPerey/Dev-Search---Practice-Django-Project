from django.shortcuts import render
from .models import Profile

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
