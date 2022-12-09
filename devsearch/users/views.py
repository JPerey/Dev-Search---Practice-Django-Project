from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, SkillForm, ProfileForm
from .utils import searchProfiles

# Create your views here.


def profiles(requests):
    profiles, search_text = searchProfiles(requests)

    context = {"profiles": profiles, "search_text": search_text}

    return render(requests, "users/profiles.html", context)


def userProfile(requests, pk):
    profileObj = Profile.objects.get(id=pk)
    context = {
        "profile": profileObj,
    }

    return render(requests, "users/user-profile.html", context)


def loginUser(requests):
    page = "login"

    if requests.user.is_authenticated:
        return redirect("profiles")

    if requests.method == "POST":
        username = requests.POST["username"]
        password = requests.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(requests, "Username does not exist")

        user = authenticate(requests, username=username, password=password)

        if user is not None:
            # <-- login function creates a session on the database for the user
            login(requests, user)
            return redirect("profiles")
        else:
            messages.error(requests, "Username or Password was incorrect.")

    context = {
        "page": page,
    }
    return render(requests, "users/login_register.html", context)


def logoutUser(requests):
    logout(requests)
    messages.success(requests, "User was succesfully logged out")
    return redirect("login")


def registerUser(requests):
    page = "register"
    form = CustomUserCreationForm()

    if requests.method == "POST":
        form = CustomUserCreationForm(requests.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # <-- this removes the
            # event where upper and lower case versions of a username exist in the same database
            user.save()

            messages.success(requests, "user account was created")
            login(requests, user)
            return redirect("userAccount")
        else:
            messages.error(requests, "An error has occurred.")

    context = {
        "page": page,
        "form": form,
    }
    return render(requests, "users/login_register.html", context)


@login_required(login_url="login")
def userAccount(requests):
    profile = requests.user.profile
    context = {
        "profile": profile,
    }

    return render(requests, "users/account.html", context)


@login_required(login_url="login")
def createSkill(requests):
    profile = requests.user.profile
    form = SkillForm()

    if requests.method == "POST":
        form = SkillForm(requests.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            # this is what sets the skill to the current logged in user
            skill.owner = profile
            skill.save()
            messages.success(requests, "Skill was added successfully!")
            return redirect("userAccount")

    context = {"form": form}
    return render(requests, "users/skill_form.html", context)


@login_required(login_url="login")
def updateSkill(requests, pk):
    profile = requests.user.profile
    skillObj = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skillObj)

    if requests.method == "POST":
        form = SkillForm(requests.POST, instance=skillObj)
        if form.is_valid():
            form.save()
            messages.success(requests, "Skill was updated!")
            return redirect("userAccount")

    context = {"form": form}
    return render(requests, "users/skill_form.html", context)


@login_required(login_url="login")
def deleteSkill(requests, pk):
    profile = requests.user.profile
    skillObj = profile.skill_set.get(id=pk)
    if requests.method == "POST":
        skillObj.delete()
        messages.success(requests, "Skill was deleted successfully!")
        return redirect("userAccount")

    context = {"skill": skillObj}
    return render(requests, "users/delete_skill_template.html", context)


@login_required(login_url="login")
def editAccount(requests):
    form = ProfileForm()
    profile = requests.user.profile

    if requests.method == "POST":
        form = ProfileForm(requests.POST, requests.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("userAccount")

    context = {"form": form}
    return render(requests, "users/delete_skill_template.html", context)
