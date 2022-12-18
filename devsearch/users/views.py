from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Message
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, SkillForm, ProfileForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.


def profiles(requests):
    profiles, search_text = searchProfiles(requests)

    custom_range, profiles = paginateProfiles(requests, profiles, 6)

    context = {
        "profiles": profiles,
        "search_text": search_text,
        "custom_range": custom_range,
    }

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
        username = requests.POST["username"].lower()
        password = requests.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(requests, "Username does not exist")

        user = authenticate(requests, username=username, password=password)

        if user is not None:
            # <-- login function creates a session on the database for the user
            login(requests, user)
            return redirect(
                requests.GET["next"] if "next" in requests.GET else "userAccount"
            )
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
    return render(requests, "users/profile_form.html", context)


@login_required(login_url="login")
def Inbox(requests):
    profile = requests.user.profile
    messageRequests = profile.messages.all()
    read_messages = profile.messages.filter(is_read=True)
    unread_messages = profile.messages.filter(is_read=False)
    unread_count = messageRequests.filter(is_read=False).count()

    context = {
        "messageRequests": messageRequests,
        "unread_count": unread_count,
        "unread_messages": unread_messages,
        "read_messages": read_messages,
    }
    return render(requests, "users/inbox.html", context)


@login_required(login_url="login")
def viewMessage(requests, pk):
    profile = requests.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {
        "message": message,
    }
    return render(requests, "users/message.html", context)


def createMessage(requests, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = requests.user.profile
    except:
        sender = None

    if requests.method == "POST":
        form = MessageForm(requests.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(requests, "message successfully sent")

            return redirect("userProfile", pk=recipient.id)

    context = {
        "form": form,
        "recipient": recipient,
    }

    return render(requests, "users/message_form.html", context)
