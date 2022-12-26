from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from django.contrib import messages
from .utils import searchProjects, paginateProjects


def projects(requests):

    projects, search_text = searchProjects(requests)

    custom_range, projects = paginateProjects(requests, projects, 6)

    context = {
        "projects": projects,
        "search_text": search_text,
        "custom_range": custom_range,
    }
    return render(requests, "projects/projects.html", context)


def project(requests, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if requests.method == "POST":
        form = ReviewForm(requests.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = requests.user.profile
        review.save()
        messages.success(requests, "your review was successfully submitted!")

        projectObj.getVoteCount

        return redirect("project", pk=projectObj.id)

    tags = projectObj.tags.all()
    return render(
        requests,
        "projects/single-project.html",
        {"project": projectObj, "tags": tags, "form": form},
    )


@login_required(login_url="login")
def createProject(requests):
    profile = requests.user.profile

    form = ProjectForm()
    if requests.method == "POST":
        # print("DATA: ", requests.POST)
        new_tags = requests.POST.get("newtags").split(",")

        form = ProjectForm(requests.POST, requests.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("projects")

    context = {"form": form}
    return render(requests, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(requests, pk):
    profile = requests.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)
    if requests.method == "POST":
        new_tags = requests.POST.get("newtags").split(",")
        # print(requests.POST)
        form = ProjectForm(requests.POST, requests.FILES, instance=projectObj)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect("projects")

    context = {"form": form}
    return render(requests, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(requests, pk):
    profile = requests.user.profile
    projectObj = profile.project_set.get(id=pk)
    if requests.method == "POST":
        projectObj.delete()
        return redirect("projects")
    context = {"object": projectObj}
    return render(requests, "projects/delete_template.html", context)
