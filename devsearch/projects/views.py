from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(requests):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(requests, "projects/projects.html", context)


def project(requests, pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    return render(
        requests, "projects/single-project.html", {
            "project": projectObj, "tags": tags}
    )


def createProject(requests):
    form = ProjectForm()
    if requests.method == "POST":
        # print(requests.POST)
        form = ProjectForm(requests.POST, requests.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(requests, "projects/project_form.html", context)


def updateProject(requests, pk):
    projectObj = Project.objects.get(id=pk)
    form = ProjectForm(instance=projectObj)
    if requests.method == "POST":
        # print(requests.POST)
        form = ProjectForm(requests.POST, requests.FILES,  instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context = {'form': form}
    return render(requests, "projects/project_form.html", context)


def deleteProject(requests, pk):
    projectObj = Project.objects.get(id=pk)
    if requests.method == "POST":
        projectObj.delete()
        return redirect('projects')
    context = {'object': projectObj}
    return render(requests, 'projects/delete_template.html', context)
