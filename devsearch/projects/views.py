from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm
from django.db.models import Q
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
    tags = projectObj.tags.all()
    return render(
        requests, "projects/single-project.html", {"project": projectObj, "tags": tags}
    )


@login_required(login_url="login")
def createProject(requests):
    profile = requests.user.profile

    form = ProjectForm()
    if requests.method == "POST":
        # print(requests.POST)
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
        # print(requests.POST)
        form = ProjectForm(requests.POST, requests.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
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
