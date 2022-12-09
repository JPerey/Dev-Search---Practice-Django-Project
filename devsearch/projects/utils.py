from django.db.models import Q
from .models import Tag, Project


def searchProjects(requests):
    search_text = ""

    if requests.GET.get("search_text"):
        search_text = requests.GET.get("search_text")

    tags = Tag.objects.filter(name__icontains=search_text)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_text) |
        Q(description__icontains=search_text) |
        Q(owner__name__icontains=search_text) |
        Q(tags__in=tags)
    )

    return projects, search_text
