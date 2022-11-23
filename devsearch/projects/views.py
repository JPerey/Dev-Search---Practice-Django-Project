from django.shortcuts import render
from django.http import HttpResponse

projectsList = [
    {
        "id": "1",
        "title": "Ecommerce Website",
        "description": "Fully functional ecommerce website",
    },
    {
        "id": "2",
        "title": "Portfolio Website",
        "description": "A personal website to write articles and display work",
    },
    {
        "id": "3",
        "title": "Social Network",
        "description": "An open source project built by the community",
    },
]


def projects(requests):
    msg_plural = "projects"
    num = 11
    context = {
        "message": msg_plural,
        "num": num,
        "projects": projectsList,
    }
    return render(requests, "projects/projects.html", context)


def project(requests, pk):
    projectObj = None

    for i in projectsList:
        if i["id"] == pk:
            projectObj = i
    return render(requests, "projects/single-project.html", {"project": projectObj})
